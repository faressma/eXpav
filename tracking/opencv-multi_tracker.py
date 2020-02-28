import cv2
import sys
import imutils
import math

major_ver, minor_ver, subminor_ver = cv2.__version__.split('.')


def create_tracker(tracker: str):
	'''Create a tracker'''
	tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
	tracker_type = tracker_types[0]

	if tracker not in tracker_types:
		print(f'error: not supported tracker \'{tracker}\', available trackers are {tracker_types}.')
		sys.exit(-1)

	if int(major_ver) == 3 and int(minor_ver) < 3:
		tracker = cv2.Tracker_create(tracker_type)
	else:
		if tracker_type == 'BOOSTING':
			tracker = cv2.TrackerBoosting_create()
		elif tracker_type == 'MIL':
			tracker = cv2.TrackerMIL_create()
		elif tracker_type == 'KCF':
			tracker = cv2.TrackerKCF_create()
		elif tracker_type == 'TLD':
			tracker = cv2.TrackerTLD_create()
		elif tracker_type == 'MEDIANFLOW':
			tracker = cv2.TrackerMedianFlow_create()
		elif tracker_type == 'GOTURN':
			tracker = cv2.TrackerGOTURN_create()
		elif tracker_type == 'MOSSE':
			tracker = cv2.TrackerMOSSE_create()
		elif tracker_type == 'CSRT':
			tracker = cv2.TrackerCSRT_create()

	return tracker


def select_bounding_boxes(frame):
	boxes = []
	infos = []
	colors = ((0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255))
	print('Press [enter] to end selection, press [space] to add an other box')
	for i, color in enumerate(colors):
		bbox = cv2.selectROI(frame, False)
		boxes.append(bbox)
		infos.append((color, f'Car {i}'))
		k = cv2.waitKey(0) & 0xff
		if k == ord('q'):
			break
	return boxes, infos


def normalize(box, scale):
	return tuple(int(a * scale) for a in box)


if __name__ == '__main__':
	# Set globals
	tracker_type = 'BOOSTING'
	# tracker_type = 'KCF'
	img_width = 300

	# Read the video
	video = cv2.VideoCapture('/home/Victor/Vidéos/car-v3.mp4')
	#video = cv2.VideoCapture(0)
	if not video.isOpened():
		print('error: could not open the video, are you sure the file exists?')
		sys.exit(-2)

	# Read first frame.
	ok, frame = video.read()
	scale = len(frame[0]) / img_width

	frame_small = imutils.resize(frame, width=img_width)
	if not ok:
		print('error: cannot read the video file')
		sys.exit(-2)

	# Select a bounding box
	boxes, infos = select_bounding_boxes(frame)
	print(f'info: {len(boxes)} boxes selected')

	# Create the multitracker
	tracker = cv2.MultiTracker_create()
	for bbox, (color, name) in zip(boxes, infos):
		print(f'info: {name}: {bbox}')
		small_bbox = normalize(bbox, 1 / scale)
		tracker.add(create_tracker(tracker_type), frame_small, small_bbox)

	cv2.imshow('[eXpav]', frame)
	cv2.waitKey(0)
	cv2.waitKey(0)


	# Prepare speed vectors
	speed_timer = cv2.getTickCount()
	centers = [((x+w) // 2, (y+h) // 2) for x, y, w, h in (normalize(box, 1 / scale) for box in boxes)]
	speed_vectors = [(0, 0) for _ in boxes]


	# For all video's frame
	while video.isOpened():
		# Read a new frame
		ok, frame = video.read()
		if not ok:
			break
		frame_small = imutils.resize(frame, width=img_width)

		# Start timer
		timer = cv2.getTickCount()

		# Update tracker
		ok, boxes = tracker.update(frame_small)

		# Calculate Frames per second (FPS), could be at the end for a more accurate
		# result, but we want to mesure the tracker's FPS impact, not the decoration.
		fps = int(cv2.getTickFrequency() / (cv2.getTickCount() - timer))

		# Update speed vectors
		if cv2.getTickCount() - speed_timer > .2 * cv2.getTickFrequency():
			new_centers = [((x+w) / 2, (y+h) / 2) for x, y, w, h in boxes]
			speed_vectors = [(nx - ox, ny - oy) for (ox, oy), (nx, ny) in zip(centers, new_centers)]
			centers = new_centers
			speed_timer = cv2.getTickCount()

		# Draw bounding box and speed vectors
		for bbox, (color, name), vec in zip(boxes, infos, speed_vectors):
			x, y, w, h = normalize(bbox, scale)
			c = (x+w // 2, y+h // 2)
			mult = 20
			to = (int(c[0] + vec[0] * mult), int(c[1] + vec[1] * mult))
			speed = int(math.sqrt(vec[0] ** 2 + vec[1] ** 2) * 5)

			cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2, 1)
			cv2.putText(frame, f'{name} ({speed}px/s)', (x+2, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
			cv2.arrowedLine(frame, c, to, color, 2, tipLength=.3)


		# General Info overlay
		cv2.putText(frame, tracker_type + ' Tracker', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
		cv2.putText(frame, f'FPS : {fps}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

		# Display result
		cv2.imshow('[eXpav]', frame)

		# Exit if ESC pressed
		k = cv2.waitKey(1) & 0xff
		if k == 27:
			break

	print('done.')
