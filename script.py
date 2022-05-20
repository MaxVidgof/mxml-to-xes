#!/usr/bin/env python3

#from models import pasreString
import sys
import xes
import os
import models

filename = sys.argv[1]

with open(filename, "r") as f:
	content = f.readlines()

content[0] = '<?xml version="1.0" ?>\n'
joined = "".join(content)
log = models.parseString(joined)

output = xes.Log()
for instance in log.Process[0].ProcessInstance:
	trace = xes.Trace()
	case = instance.get_id()
	trace.add_attribute(xes.Attribute(type="string", key="concept:name", value=case))
	for event in instance.AuditTrailEntry:
		e = xes.Event()
		activity = event.get_WorkflowModelElement()
		e.add_attribute(xes.Attribute(type="string", key="concept:name", value=activity))
		event_type = event.get_EventType().get_valueOf_()
		e.add_attribute(xes.Attribute(type="string", key="lifecycle:transition", value=event_type))
		timestamp = event.Timestamp.get_valueOf_()
		e.add_attribute(xes.Attribute(type="date", key="time:timestamp", value=timestamp))
		attributes = {}
		for attribute in event.Data.Attribute:
			attributes[attribute.get_name()]=attribute.get_valueOf_()
		for key,value in attributes.items():
			e.add_attribute(xes.Attribute(type="string", key=key, value=value))
		trace.add_event(e)
	output.add_trace(trace)

base_filename = ".".join(os.path.basename(filename).split('.')[0:-1])
#output_filename = filename.replace(".mxml",".xes")
output_filename = base_filename+".xes"
with open(output_filename, "w") as f:
	f.write(str(output))
