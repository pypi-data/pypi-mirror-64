# Copyright © 2020 Noel Kaczmarek
from spyne import Unicode, Integer
from spyne.model.complex import ComplexModel


UUID = Unicode(32, type_name='UUID')


class ServiceType(ComplexModel):
    id = Integer
    name = Unicode
    port = Integer


class Service(ComplexModel):
    id = UUID
    host = Unicode
    type = ServiceType


MandatoryServiceType = ServiceType.customize(nullable=False, min_occurs=1)
MandatoryService = Service.customize(nullable=False, min_occurs=1)