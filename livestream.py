# import the necessary packages
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import random

# options are:
# 'w' for wong_halves ---- level 3
# 'z' for zen_count ---- level 2
# 'h' for hi_lo ---- level 1
style = 'z'

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input video")
ap.add_argument("-o", "--output", required=True,
	help="path to output video")
ap.add_argument("-y", "--yolo", required=True,
	help="base path to YOLO directory")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
ap.add_argument("-t", "--threshold", type=float, default=0.3,
	help="threshold when applyong non-maxima suppression")
args = vars(ap.parse_args())

# load the COCO class labels our YOLO model was trained on
labelsPath = os.path.sep.join([args["yolo"], "obj.names"])
LABELS = open(labelsPath).read().strip().split("\n")
# initialize a list of colors to represent each possible class label
np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")
# derive the paths to the YOLO weights and model configuration
weightsPath = os.path.sep.join([args["yolo"], "yolo-obj_5100.weights"])
configPath = os.path.sep.join([args["yolo"], "yolo-obj.cfg"])
# load our YOLO object detector trained on COCO dataset (80 classes)
# and determine only the *output* layer names that we need from YOLO
print("[INFO] loading YOLO from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# initialize the video stream, pointer to output video file, and
# frame dimensions
vs = cv2.VideoCapture(0) # replace with live stream
#vs = cv2.VideoCapture(args["input"])
writer = None
(W, H) = (None, None)
# try to determine the total number of frames in the video file
try:
	prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
		else cv2.CAP_PROP_FRAME_COUNT
	total = int(vs.get(prop))
	print("[INFO] {} total frames in video".format(total))
# an error occurred while trying to determine the total
# number of frames in the video file
except:
	print("[INFO] could not determine # of frames in video")
	print("[INFO] no approx. completion time can be provided")
	total = -1

cardToNum = {'A': 1,'J': 10, 'Q': 10, 'K': 10, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10}
for i in range(2,11):
	cardToNum[i] = i

frame_unchanged = 0
cards_played = {}
for n in ['A', *range(2,11), 'J', 'Q', 'K']:
	for s in ['d', 'h', 's', 'c']:
		cards_played[str(n)+s] = 0

dealer = 0
player = 0
curr_cardcount = 0

#stability algorithm data structures
frame_unchanged = 0
cards_detected = []

# Dictioanry keys: 
# counting system (ex: wong halves) -> point values -> card ranks that associate with those values
counting_style = {'w': {.5:{'2','7'}, 1:{'3','4','6'}, 1.5:{'5'}, -.5:{'9'}, -1:{'10', 'J', 'Q', 'K', 'A'}, 0:{'8'}}, 
				  'z': {1:{'2','3','7'}, -1:{'A'}, 2:{'4','5','6'}, -2:{'10', 'J', 'Q', 'K'}, 0:{'8','9'}}, 
				  'h': {1:{'2','3','4','5','6'}, 0:{'7','8','9'}, -1:{'A', '10', '9', '8', 'J', 'Q', 'K'}}
				 }

# loop over frames from the video file stream
while True:
	# read the next frame from the file
	(grabbed, frame) = vs.read()
	print('read')
	# if the frame was not grabbed, then we have reached the end
	# of the stream
	
	if not grabbed:
		break
	# if the frame dimensions are empty, grab them
	frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
	if W is None or H is None:
		(H, W) = frame.shape[:2]
# construct a blob from the input frame and then perform a forward
	# pass of the YOLO object detector, giving us our bounding boxes
	# and associated probabilities
	blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
		swapRB=True, crop=False)
	net.setInput(blob)
	start = time.time()
	layerOutputs = net.forward(ln)
	end = time.time()

	# initialize our lists of detected bounding boxes, confidences,
	# and class IDs, respectively
	boxes = []
	confidences = []
	classIDs = []

	# loop over each of the layer outputs
	for output in layerOutputs:
		# loop over each of the detections
		for detection in output:
			# extract the class ID and confidence (i.e., probability)
			# of the current object detection
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]
			# filter out weak predictions by ensuring the detected
			# probability is greater than the minimum probability
			if confidence > args["confidence"]:
				# scale the bounding box coordinates back relative to
				# the size of the image, keeping in mind that YOLO
				# actually returns the center (x, y)-coordinates of
				# the bounding box followed by the boxes' width and
				# height
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")
				# use the center (x, y)-coordinates to derive the top
				# and and left corner of the bounding box
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))
				# update our list of bounding box coordinates,
				# confidences, and class IDs
				boxes.append([x, y, int(width), int(height)])
				confidences.append(float(confidence))
				classIDs.append(classID)
	# apply non-maxima suppression to suppress weak, overlapping
	# bounding boxes
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],
		args["threshold"])
	# ensure at least one detection exists
	if len(idxs) > 0:
		cards_detected_now = []
		# loop over the indexes we are keeping
		for i in idxs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])
			print(LABELS[classIDs[i]], x, y, w, h, W, H)
			cards_detected_now.append(LABELS[classIDs[i]])
			# draw a bounding box rectangle and label on the frame
			
			if not cards_played[LABELS[classIDs[i]]]:
				frame_unchanged = 0
				if y+h/2 > H/2: # if card is on bottom side of the screen
					player += cardToNum[LABELS[classIDs[i]][0]]
				else: # assume that dealer is on top side of screen
					dealer += cardToNum[LABELS[classIDs[i]][0]]
				cards_played[LABELS[classIDs[i]]] = 1

				for point_val in counting_style[style]:
					if LABELS[classIDs[i]][0] in counting_style[style][point_val]:
						curr_cardcount += point_val

			color = [int(c) for c in COLORS[classIDs[i]]]
			cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
			text = "{}: {:.4f}".format(LABELS[classIDs[i]],
				confidences[i])
			cv2.putText(frame, text, (x, y - 5),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
		cards_detected_now.sort()
		cards_detected.sort()
		if cards_detected_now == cards_detected:
			frame_unchanged += 1
		if frame_unchanged == 5:
			print(player, dealer, curr_cardcount, ('stable', 'unstable')[frame_unchanged == 0])
			if random.random() > 0.5:
				print('hit')
			else:
				print('stand')
			frame_unchanged = 0
		elif frame_unchanged == 0:
			cards_detected = cards_detected_now
	else:
			frame_unchanged = 0



	# check if the video writer is None
	if writer is None:
		# initialize our video writer
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 30,
			(frame.shape[1], frame.shape[0]), True)
		# some information on processing single frame
		if total > 0:
			elap = (end - start)
			print("[INFO] single frame took {:.4f} seconds".format(elap))
			print("[INFO] estimated total time to finish: {:.4f}".format(
				elap * total))
	# write the output frame to disk
	cv2.imshow('Input', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# release the file pointers
print("[INFO] cleaning up...")
# writer.release()
vs.release()

#            ch = 0xFF & cv2.waitKey(1000)