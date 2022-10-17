from .models import ProfileUserModel,ShopCellModel
from django.contrib.auth.models import User
from mimesis import Person,Address,Hardware,Finance
from mimesis.locales import Locale
from django.db import Error,transaction


# Clases

class GeneratorDataDB(object):
    person_faker = Person(locale=Locale.ES)
    address_faker = Address(locale=Locale.ES)
    phone_faker = Hardware()
    price_faker = Finance()


    def generator(self,number:int) -> None:
        articules_per_users = number // 8
        password = "password01"
        text_phone:str
        address:str

        for n in range(1,number):
            point_db = transaction.savepoint()
            user = User()
            user.username = self.person_faker.username()
            user.first_name = self.person_faker.first_name()
            user.last_name = self.person_faker.last_name()
            user.email = self.person_faker.email(domains=['gmail.com','yahoo.com','nauta.cu'])
            user.set_password(password)
            try:
                user.save()
                address = """{} {} {} {} {}""".format(self.address_faker.province(),
                                                      self.address_faker.city(),
                                                      self.address_faker.state(),
                                                      self.address_faker.street_name(),
                                                      self.address_faker.street_number())
                ProfileUserModel.objects.create(
                    user=user,phone=self.person_faker.telephone(mask="5#######"),
                    address=address
                )
                for a in range(1,articules_per_users):
                    text_phone = \
                    """Pantalla: {}\nResolución: {}\nProvedor: {}\nTamaño de Ram: {}\nModelo CPU: {}\nFrecuencia CPU: {}""".\
                    format(self.phone_faker.screen_size(),
                        self.phone_faker.resolution(),
                        self.phone_faker.manufacturer(),
                        self.phone_faker.ram_size(),
                        self.phone_faker.cpu_model_code(),
                        self.phone_faker.cpu_frequency())

                    ShopCellModel.objects.create(
                        profile=user.profile,
                        model_name=self.phone_faker.phone_model(),
                        price=int(self.price_faker.price(minimum=150,maximum=2000)),
                        description=text_phone)

            except Error:
                transaction.savepoint_rollback(point_db)
        
        print("Generator successful!")

            


               
                





      

