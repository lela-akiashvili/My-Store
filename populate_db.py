import os
import django
from datetime import date

# ვეუბნებით პითონს თუ სად იპოვოს Django-ს პარამეტრები
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_store.settings")
django.setup()

# ვაიმპორტებთ ჩვენს მოდელს
from core.models import Item, ItemReview

def populate():
    print("ვასუფთავებ ძველ მონაცემებს (თუ არსებობს)...")
    Item.objects.all().delete()
    
    print("ვიწყებ ახალი ნივთების დამატებას...")
    
    products = [
        {"name": "თანამედროვე დივანი 'ალფა'", "brand": "IKEA", "category": "ავეჯი", "price": 1200.00, "stock": 5, "date": date(2023, 5, 10), "desc": "კომფორტული, 3-ადგილიანი დივანი ნაცრისფერი ნაჭრით."},
        {"name": "ხის სასადილო მაგიდა", "brand": "JYSK", "category": "ავეჯი", "price": 850.50, "stock": 12, "date": date(2023, 8, 15), "desc": "მუხის მასიური ხისგან დამზადებული მაგიდა, იტევს 6 ადამიანს."},
        {"name": "მინიმალისტური სავარძელი", "brand": "IKEA", "category": "ავეჯი", "price": 450.00, "stock": 8, "date": date(2024, 1, 20), "desc": "ყვითელი ფერის ერგონომიული სავარძელი დასვენებისთვის."},
        {"name": "კერამიკული ლარნაკი", "brand": "HomeDecor", "category": "დეკორი", "price": 45.00, "stock": 30, "date": date(2023, 11, 5), "desc": "ხელით მოხატული კერამიკული ლარნაკი ყვავილებისთვის."},
        {"name": "აბსტრაქტული კედლის ნახატი", "brand": "ArtStudio", "category": "დეკორი", "price": 120.00, "stock": 15, "date": date(2023, 2, 10), "desc": "ტილოზე შესრულებული აბსტრაქტული ნახატი, 60x90 სმ."},
        {"name": "კუთხის სანათი 'ლუნა'", "brand": "Philips", "category": "განათება", "price": 180.00, "stock": 20, "date": date(2023, 9, 1), "desc": "თბილი ნათების მქონე იატაკის სანათი."},
        {"name": "ბამბუკის სარკე", "brand": "JYSK", "category": "დეკორი", "price": 85.00, "stock": 25, "date": date(2023, 12, 12), "desc": "მრგვალი კედლის სარკე ბამბუკის ჩარჩოთი."},
        {"name": "ჟურნალების მაგიდა", "brand": "IKEA", "category": "ავეჯი", "price": 150.00, "stock": 18, "date": date(2024, 2, 28), "desc": "შუშის ზედაპირიანი პატარა მაგიდა მისაღები ოთახისთვის."},
        {"name": "დეკორატიული ბალიშების ნაკრები", "brand": "HomeDecor", "category": "ტექსტილი", "price": 60.00, "stock": 40, "date": date(2023, 10, 15), "desc": "3 ცალი ბალიში გეომეტრიული ფიგურებით."},
        {"name": "ხალიჩა 'მონოკრომი'", "brand": "CarpetLine", "category": "ტექსტილი", "price": 320.00, "stock": 10, "date": date(2023, 7, 7), "desc": "შავ-თეთრი რბილი ხალიჩა, 160x230 სმ."},
        {"name": "სამუშაო მაგიდა", "brand": "IKEA", "category": "ავეჯი", "price": 380.00, "stock": 14, "date": date(2023, 4, 18), "desc": "თეთრი ფერის მაგიდა კომპიუტერისთვის უჯრებით."},
        {"name": "საოფისე სკამი", "brand": "OfficePlus", "category": "ავეჯი", "price": 250.00, "stock": 22, "date": date(2023, 6, 25), "desc": "გორგოლაჭებიანი, რეგულირებადი სკამი."},
        {"name": "კედლის საათი", "brand": "TimePiece", "category": "დეკორი", "price": 55.00, "stock": 35, "date": date(2024, 1, 5), "desc": "მინიმალისტური დიზაინის უხმაურო კედლის საათი."},
        {"name": "წიგნების თარო", "brand": "JYSK", "category": "ავეჯი", "price": 210.00, "stock": 9, "date": date(2023, 3, 30), "desc": "5 სართულიანი ხის თარო წიგნებისა და დეკორაციებისთვის."},
        {"name": "მაგიდის სანათი", "brand": "Philips", "category": "განათება", "price": 95.00, "stock": 28, "date": date(2023, 11, 20), "desc": "სენსორული სანათი სამუშაო მაგიდისთვის."}
    ]

    for p in products:
        item = Item.objects.create(
            name=p["name"],
            brand=p["brand"],
            category=p["category"],
            price=p["price"],
            stock_quantity=p["stock"],
            release_date=p["date"],
            description=p["desc"]
        )
        # დავუმატოთ 1 ცალი სატესტო რევიუ თითოეულს, რომ რეიტინგი გამოჩნდეს
        ItemReview.objects.create(
            item=item,
            reviewer_name="მომხმარებელი",
            rating_stars=5,
            comment="ძალიან კარგი ხარისხის ნივთია!"
        )
        print(f"დაემატა: {item.name}")

    print("--- ოპერაცია წარმატებით დასრულდა! 15 ნივთი ჩაიწერა ბაზაში. ---")

if __name__ == '__main__':
    populate()