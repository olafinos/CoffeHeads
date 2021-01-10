import os
import sys
import random
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
PROJECT_PATH = os.path.split(SCRIPT_PATH)[0]
sys.path.insert(0,PROJECT_PATH)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','mysite.settings')
import django
django.setup()
from django.contrib.auth.models import User
from coffeeheads.models import Coffee, Opinion, UserCoffee
from coffeeheads.views import AddUserCoffee

ORIGIN = ['Gwatemala','Peru','Brazil','Honduras','Mexico','Argentina','Costa Rica',"Etiopia","Salwador",'Trinidad & Tobago',"India","Tanzania"]
MANUFACTURE = ["Duka", "Early Bird", "HAYB", "Grano", "Blueberry Roasters", "Hard Beans"]
DESCRIPTION = ["This coffee is our most complex in terms of blend makeup and contains a range of origins, varietals, and processing methods. Supreme displays a full-bodied richness, a crisp, cradling acidity, and lingering cocoa finish. ", "A blend of several excellent, roasted medium-dark to give a milk chocolate cup, a smooth silky body and a long finish. Lower in acidity, this Blend makes plush espresso and mixes well in milk drinks.",
               "Blend designed with the espresso drinker in mind. With its distinctive dark chocolate notes, full body and pleasant finish, this blend makes gutsy milk drinks, and hefty espresso.","A fully washed Arabica, one of the first “new world” homes of coffee. Our Mt. Raung Java has a heavy, creamy body, a soft cradling acidity and pleasant sweetness. It has a familiar earthy complexity but is delivered very cleanly, with toast and baker’s chocolate notes to boot."
               ,"This washed espresso delivers all the great characteristics we know and love about coffee. Expect a perfumed citrus aroma with sweet fruit tones, a silky chocolate body and a refreshing lime marmalade finish."]
USERNAMES = ["Bob1337","Andrzejek","Ricardo232","Carl432","JoshuaxCoff","TruniaGrunia","BuniaMischigan","PotHead","MichelAngelo132"]
OPINIONS = ["The coffee is delicate, not too acidic, the espresso I brew from it is good, although you don't feel the strength of the coffee, which may be an obstacle for some.",
            "The coffee is very tasty, mild, without acidity. Strong but mild in flavor. We brew in an automatic pressure grinding machine, the coffee has a delicate foam.",
            "A uniquely structured naturally processed coffee that delivers sweet-tart, fruit-centered richness, juicy-bright acidity, vibrantly viscous mouthfeel. An intricately layered roller coaster of sensory pleasures.",
            "Delicately sweet-tart, richly and intricately aromatic, deep-toned. Dried hibiscus flowers, bergamot, frankincense, lychee, boysenberry in aroma and cup. Confidently sweet-tart structure with sparkling acidity; silky, buoyant mouthfeel. The long, lingering flavor-saturated finish intoxicatingly blurs fruit and floral notes.",
            " A celebratory coffee — invitingly chocolaty and rich with a whisper of Cognac underneath lush suggestions of tropical fruit.",
            "Aromatically tropical, deeply floral, mysteriously complex. Plumeria, amber, passion fruit, Concord grape, dark chocolate in aroma and cup. Deep-toned, sweetly savory structure with winy acidity; decadently plush mouthfeel. The finish goes on and on.",
            "Very sweet, high-toned, richly floral. Star jasmine, lemon verbena, pineapple, cocoa nib, frankincense in aroma and cup. Sweetly tart structure with juicy, levitating acidity; delicate but syrupy mouthfeel. Crisp, long, floral-toned finish.",
            "Bright yet deep-toned, sweet-tart-savory, intensely floral. Mango, dark chocolate, hop flowers, lilac, wild honey in aroma and cup. Richly bittersweet structure with juicy-bright acidity; viscous, nectar-like mouthfeel. Flavor-saturated, chocolaty finish.",
            "Deeply sweet, richly tart, harmoniously balanced. Dried mango, dark chocolate, brown sugar, oolong tea, tangerine zest in aroma and cup. Sweet-tart structure with citrusy-bright acidity; full, round, syrupy mouthfeel. Lingeringly sweet, tropical fruit-driven finish.",
            "Delicate, tropical, fruity and floral. Strawberry guava, bergamot, cocoa nib, sandalwood, plumeria in aroma and cup. Sweet-toned structure with juicy, vibrant acidity; silky, buoyant mouthfeel. Resonant, flavor-saturated, very long finish.",
            "Deep, intense, sweet-savory, utterly coherent. Intense lavender, black currant, mandarin orange, sandalwood, dark chocolate in aroma and cup. Sweet, tart, savory-bottomed structure with intense, balanced acidity; big, mouth-filling body. The flavor-saturated finish carries over every nuance from the cup."]
def create_coffees(origin, manufacture, description, number_of_items):
    """
    Creates random coffees from given lists with possible names.
    :param origin: List with origins
    :param manufacture: List with manufactures
    :param description: List with descriptions
    :param number_of_items: Number of coffees which will be created
    """
    absolute_path = os.path.join(PROJECT_PATH,'media','img')
    images_paths = os.listdir(absolute_path)
    for _ in range(number_of_items):
        rand_origin = random.choice(origin)
        rand_manu = random.choice(manufacture)
        rand_desc = random.choice(description)
        rand_image_path = os.path.join(absolute_path, random.choice(images_paths))
        price = float("{:.2f}".format(random.uniform(15,30)))
        name = f"{rand_manu} {rand_origin}"
        c = Coffee(name=name,origin=rand_origin,manufacturer=rand_manu,description=rand_desc,estimated_price=price,image=rand_image_path)
        c.save()
    return images_paths

def create_users(usernames,opinions):
    """
    Creates users with their random coffee history and opinions
    :param usernames: List of usernames
    :param opinions: List with possible opinions
    """
    for username in usernames:
        email = f"{username}@mail.com"
        password = "Password123"
        user = User.objects.create_user(username=username,email=email,password=password)
        number_of_coffees = random.randint(3,12)
        coffees = Coffee.objects.filter()
        random_coffees = random.sample(list(coffees),number_of_coffees)
        for coffee in random_coffees:
            rating = float("{:.2f}".format(random.uniform(5, 10)))
            acidity = random.randint(0,10)
            body = random.randint(0, 10)
            flavor = random.randint(0, 10)
            bitterness = random.randint(0, 10)
            opinion_desc = random.choice(opinions)
            opinion = Opinion(coffee=coffee, user=user,rating=rating, acidity=acidity,
                              body=body,flavor=flavor,bitterness=bitterness,opinion=opinion_desc)
            opinion.save()
            user_coffe = UserCoffee(owner=user,coffee=coffee,opinion=opinion)
            user_coffe.save()
            AddUserCoffee.update_average(coffee=coffee)

if __name__ == '__main__':
    images = create_coffees(ORIGIN,MANUFACTURE,DESCRIPTION,35)
    create_users(USERNAMES,OPINIONS)
    print(images)