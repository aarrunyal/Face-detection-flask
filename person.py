class Person:
    def __init__(self,id,  name, age, email, image) -> None:
        self.id =id
        self.name = name
        self.age = age
        self.email = email
        self.image = image

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "image": self.image
        }
