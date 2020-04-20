#DATE_FORMAT = '%Y-%m-%d'
#TIME_FORMAT = '%H:%M:%S'
import re
CAPTURE_FILE_FORMAT = '%Y-%m-%d/capture_%H:%M:%S.png'
CAPTURE_FILE_REGEX =  re.compile('.*(\d{4}-\d{2}-\d{2}/capture_\d{2}:\d{2}:\d{2}.png)')
CAPTURE_FILE_GLOB = '**/capture*.png' 
