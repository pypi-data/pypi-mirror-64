from uuid import uuid5, NAMESPACE_URL

from peto.domainmodel.base import PetoAggregateRoot


class Person(PetoAggregateRoot):
    def __init__(
        self, name, dob, nhs_num, tel_num, email, postcode, house_num, **kwargs
    ):
        super(Person, self).__init__(**kwargs)
        self.name = name
        self.dob = dob
        self.nhs_num = nhs_num
        self.tel_num = tel_num
        self.email = email
        self.postcode = postcode
        self.house_num = house_num

    def change_address(self, new_postcode, new_house_num):
        self.__trigger_event__(
            self.AddressChanged,
            nhs_num=self.nhs_num,
            old_postcode=self.postcode,
            old_house_num=self.house_num,
            new_postcode=new_postcode,
            new_house_num=new_house_num,
        )

    class AddressChanged(PetoAggregateRoot.Event):
        @property
        def new_postcode(self):
            return self.__dict__["new_postcode"]

        @property
        def new_house_num(self):
            return self.__dict__["new_house_num"]

        @property
        def old_postcode(self):
            return self.__dict__["old_postcode"]

        @property
        def old_house_num(self):
            return self.__dict__["old_house_num"]

        def mutate(self, obj: "Person") -> None:
            obj.postcode = self.new_postcode
            obj.house_num = self.new_house_num


def create_person_id(nhs_num):
    return uuid5(NAMESPACE_URL, f"/person/{nhs_num}")
