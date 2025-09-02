import requests

def get_vacancies():
    response = requests.get("https://api.hh.ru/vacancies", params={
        "text": "Инженер",
        "area": 2, 
        "per_page": 4
    }).json()

    for v in response["items"]:
        print("\n" + "="*50)
        print(f"вакансия: {v['name']}")
        print(f"компания: {v['employer']['name']}")
        print(f"город: {v['area']['name']}")
        
        # зп
        salary = v.get('salary')
        if salary:
            salary_from = salary.get('from', '?')
            salary_to = salary.get('to', '?')
            currency = salary.get('currency', '')
            print(f"зп: {salary_from} → {salary_to} {currency}")
        else:
            print("зп не указана")
            
        print(f"размещение вакансии: {v['published_at'][:10]}")
        print(f"ссылка: {v['alternate_url']}")

get_vacancies()