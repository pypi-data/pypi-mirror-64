# GOSH-FHIRworks2020-SkypeURI Project Descrpition

This is a simple API that generates URIs to Skype group chats/calls given a list of FHIR patients UUIDs.

### Create a (group) video call
```
  >> from SkypeURI import SkypeURI
  >> patient1UUID = '8f789d0b-3145-4cf2-8504-13159edaa747'
  >> patient2UUID = '4a064229-2a40-45f4-a259-f4eedcfd525a'
  >> patientUUIDs = [patient1UUID, patient2UUID]
  >> SkypeURI().getSkypeVideoURI(patientUUIDs)
```

### Create a (group) voice call
```
  >> from SkypeURI import SkypeURI
  >> patient1UUID = '8f789d0b-3145-4cf2-8504-13159edaa747'
  >> patient2UUID = '4a064229-2a40-45f4-a259-f4eedcfd525a'
  >> patientUUIDs = [patient1UUID, patient2UUID]
  >> SkypeURI().getSkypeVoiceURI(patientUUIDs)
```

### Create a group chat
```
  >> from SkypeURI import SkypeURI
  >> patient1UUID = '8f789d0b-3145-4cf2-8504-13159edaa747'
  >> patient2UUID = '4a064229-2a40-45f4-a259-f4eedcfd525a'
  >> patientUUIDs = [patient1UUID, patient2UUID]
  >> SkypeURI().getSkypeVideoURI(patientUUIDs)
```
