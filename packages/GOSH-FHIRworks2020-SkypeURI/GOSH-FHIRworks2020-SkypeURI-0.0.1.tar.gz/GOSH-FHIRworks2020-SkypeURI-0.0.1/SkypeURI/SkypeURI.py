from fhir_parser import FHIR
from typing import List

import json

class SkypeURI:
    def __getSkypePrefixURI(self, patientUUIDs: List[str]):
        url = "skype:"
        for index, patientUUID in enumerate(patientUUIDs):
            if index == 9:
                break

            patient = FHIR().get_patient(patientUUID)
            url += "+1" + str(patient.telecoms[0].number).replace("-", "")
            url += ";"
            

        if (url[-1] == ';'):
            url = url[:-1]

        return url

    def getSkypeVoiceURI(self, patientUUIDs: List[str]):
        url = self.__getSkypePrefixURI(patientUUIDs)
        url += "?call"
        return url

    def getSkypeVideoURI(self, patientUUIDs: List[str]):
        url = self.__getSkypePrefixURI(patientUUIDs)
        url += "?call&amp;video=true"
        return url

    def getSkypeChatURI(self, patientUUIDs: List[str]):
        url = self.__getSkypePrefixURI(patientUUIDs)
        url += "?chat&amp;topic=Group%20Chat"
        return url
        

