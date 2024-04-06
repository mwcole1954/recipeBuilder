from collections import defaultdict


class WalkJson:

    def __init__(self, data):
        self.def_dict = defaultdict()
        self.data = data
        self.count = WalkJson.counter()
        self.keys = [
            'headline', 'name', 'description',
            'totalTime', 'recipeYield', 'recipeCategory', 'cookTime', 'prepTime',
            'nutrition',
            'recipeIngredient',
            'recipeInstructions',
        ]
        # nutrition is a dict
        # ingredients is a list
        # instruction is a list of dicts or just look for text keys

    def walk_json(self, data=None):
        if not data:
            data = self.data
        if isinstance(data, list):
            self.walk_list(data)
        elif isinstance(data, dict):
            self.walk_dict(data)

    def walk_list(self, data):
        for item in data:
            if isinstance(item, list):
                self.walk_list(item)
            elif isinstance(item, dict):
                self.walk_dict(item)

    def walk_dict(self, data):
        for k, v in data.items():
            if k in self.def_dict:
                self.def_dict[f"{k}{next(self.count)}"] = v
            else:
                self.def_dict[k] = v
            if isinstance(v, list):
                self.walk_list(v)
            elif isinstance(v, dict):
                self.walk_dict(v)

    @staticmethod
    def counter():
        num = 0
        while True:
            num += 1
            yield num


if __name__ == "__main__":
    json_data = {"@context":"https://schema.org/","@type":"Recipe","description":"Loved it...just did tuna...after baking some, I finished in my cast iron griddle for creating grill marks...made it look for appetizing.","image":["https://lh3.googleusercontent.com/vKCBA-LQt_dEhpiEE_wS3eQqmNP4ZhB1lpGjmSQ-yqP5EmvYMV7dXzAHzWPvvPcDPdep6cbr_G3Tocc1EBOCbA=w1280-h1280-c-rj-v1-e365","https://lh3.googleusercontent.com/vKCBA-LQt_dEhpiEE_wS3eQqmNP4ZhB1lpGjmSQ-yqP5EmvYMV7dXzAHzWPvvPcDPdep6cbr_G3Tocc1EBOCbA=w1280-h960-c-rj-v1-e365","https://lh3.googleusercontent.com/vKCBA-LQt_dEhpiEE_wS3eQqmNP4ZhB1lpGjmSQ-yqP5EmvYMV7dXzAHzWPvvPcDPdep6cbr_G3Tocc1EBOCbA=w1280-h720-c-rj-v1-e365"],"mainEntity":"true","name":"Oven Baked Tuna Steak Dinner Twenty-five Minutes","author":{"@type":"Person","name":"Poppop Cooks"},"totalTime":"PT25M","recipeYield":4,"nutrition":{"@type":"NutritionInformation","calories":"360 calories","carbohydrateContent":"6 grams","cholesterolContent":"40 milligrams","fatContent":"27 grams","fiberContent":"2 grams","proteinContent":"24 grams","saturatedFatContent":"5 grams","sodiumContent":"750 milligrams","sugarContent":"1 grams"},"aggregateRating":{"@type":"AggregateRating","bestRating":5,"worstRating":1,"ratingValue":4.857142857142857,"reviewCount":7},"reviews":[{"@type":"Review","dateCreated":"2023-03-21","reviewBody":"I’ve made this quite a few times. Great flavor, just don’t over cook it.","author":{"@type":"Person","name":"Mr.Crowder"},"itemReviewed":{"@type":"Thing","name":"Oven Baked Tuna Steak Dinner Twenty-five Minutes"},"reviewRating":{"@type":"Rating","bestRating":5,"worstRating":1,"ratingValue":5}},{"@type":"Review","dateCreated":"2022-01-16","reviewBody":"This was the best tuna steak dinner I have ever had. Unfortunately I did not have any dill but used parsley instead and it came out beyond amazing. We all went back for seconds and thirds and my family has told me I need to make this more often.","author":{"@type":"Person","name":"YumChef-EOzQ4"},"itemReviewed":{"@type":"Thing","name":"Oven Baked Tuna Steak Dinner Twenty-five Minutes"},"reviewRating":{"@type":"Rating","bestRating":5,"worstRating":1,"ratingValue":5}},{"@type":"Review","dateCreated":"2020-11-18","reviewBody":"Very good! Would make again.","author":{"@type":"Person","name":"GlenF"},"itemReviewed":{"@type":"Thing","name":"Oven Baked Tuna Steak Dinner Twenty-five Minutes"},"reviewRating":{"@type":"Rating","bestRating":5,"worstRating":1,"ratingValue":4}},{"@type":"Review","dateCreated":"2020-11-14","reviewBody":"I made just the tuna. But it’s one of the best/simplest recepies i found. I used a bit more salt and the garlic powder, and it was great. As i’m not a fan of soy sauce tuna, so this was a gem for me. My husband liked it, which is also rear. He was never a fan of tuna.","author":{"@type":"Person","name":"ZivileKaziukonyte"},"itemReviewed":{"@type":"Thing","name":"Oven Baked Tuna Steak Dinner Twenty-five Minutes"},"reviewRating":{"@type":"Rating","bestRating":5,"worstRating":1,"ratingValue":5}},{"@type":"Review","dateCreated":"2020-02-04","reviewBody":"Loved it! Very easy to make.","author":{"@type":"Person","name":"AllstarCook1092"},"itemReviewed":{"@type":"Thing","name":"Oven Baked Tuna Steak Dinner Twenty-five Minutes"},"reviewRating":{"@type":"Rating","bestRating":5,"worstRating":1,"ratingValue":5}},{"@type":"Review","dateCreated":"2019-07-09","reviewBody":"Loved it...just did tuna...after baking some, I finished in my cast iron griddle for creating grill marks...made it look for appetizing.","author":{"@type":"Person","name":"LindaStancill99547"},"itemReviewed":{"@type":"Thing","name":"Oven Baked Tuna Steak Dinner Twenty-five Minutes"},"reviewRating":{"@type":"Rating","bestRating":5,"worstRating":1,"ratingValue":5}},{"@type":"Review","dateCreated":"2019-02-18","reviewBody":"I only made the tuna. Was very tasty and moist. I basted mine half-way thru cooking.","author":{"@type":"Person","name":"SharpFoodie5721"},"itemReviewed":{"@type":"Thing","name":"Oven Baked Tuna Steak Dinner Twenty-five Minutes"},"reviewRating":{"@type":"Rating","bestRating":5,"worstRating":1,"ratingValue":5}}],"recipeCategory":["Main Dishes"],"keywords":"Main Dishes, Source of Omega-3s, Low Sugar, Low Carb, Low Calorie, High Vitamin D, High Vitamin C, High Protein","recipeIngredient":["12 ounces tuna steaks approximately 1\" thick","1 fresh lemon ","6 tablespoons extra virgin olive oil divided","1 teaspoon salt divided","1/2 teaspoon black pepper divided","1 teaspoon dried dill weed ","12 stalks fresh asparagus ","1 teaspoon garlic powder ","1/3 cup grated Parmesan cheese "],"dateModified":"2023-11-25"}
    walk = WalkJson(json_data)
    walk.walk_json()
    for k, v in walk.def_dict.items():
        for key in walk.keys:
            if key in k:
                print(f"{k}: {v}")
