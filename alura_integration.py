import requests
import json
import time

# Configurações
ALURA_API_URL = 'https://www.alura.com.br/api/dashboard/1ce5770254d62b590738cee6a5ebc273e62e2f7a32c58fa02452e2fa232ae1c0'
CLICKUP_LIST_ID = '901105126642'  
CLICKUP_API_URL = f'https://api.clickup.com/api/v2/list/{CLICKUP_LIST_ID}/task'
API_KEY = 'pk_2142600060_YMK5RONMHWA264K0Y0J8HC7AO9N90UZ6'  
ALURA_AUTH_TOKEN = '38b54ecaceae5374bf64682e7b0d433bd5f45fe3d9326c7a93455559e117ecb51ce5770254d62b590738cee6a5ebc273e62e2f7a32c58fa02452e2fa232ae1c0'  

def get_courses_from_alura():
    headers = {
        'Authorization': f'Bearer {ALURA_AUTH_TOKEN}'
    }
    
    response = requests.get(ALURA_API_URL, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Retorna os dados obtidos
    else:
        print(f"Erro ao obter dados da Alura: {response.status_code} - {response.text}")
        return None  # Retorna None em caso de erro

def get_existing_cards_from_clickup():
    headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY
    }
    
    response = requests.get(CLICKUP_API_URL, headers=headers)
    
    if response.status_code == 200:
        return response.json()['tasks']  # Retorna as tarefas existentes
    else:
        print(f"Erro ao obter tarefas do ClickUp: {response.status_code} - {response.text}")
        return []

def create_card_in_clickup(course):
    if 'guides' in course:  # Se for um guide
        payload = {
            'name': course['name'],  # Nome do guia
            'description': f"Total de cursos: {course['totalCourses']}\nCursos concluídos: {course['completedCourses']}\nURL do curso: {course['url']}",
            'status': 'to do',  # Altere conforme necessário
        }
    else:  # Se for um course progress
        payload = {
            'name': course['name'],  # Aqui usamos 'name' apenas para cursos
            'description': f"Progresso: {course.get('progress', 0)}%\nÚltimo acesso: {time.strftime('%d/%m/%Y', time.localtime(course.get('lastAccessTime', 0) / 1000))}",
            'status': 'to do',  # Altere conforme necessário
        }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": API_KEY
    }
    
    response = requests.post(CLICKUP_API_URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        task = response.json()
        print(f"Card criado com sucesso: {course.get('name', course.get('name'))}")  # Usando 'name' ou 'name'
        return task['id']  # Retorna o ID da tarefa criada
    else:
        print("Erro ao criar o card:", response.json())
        return None

def delete_task_in_clickup(task_id):
    delete_url = f'https://api.clickup.com/api/v2/task/{task_id}'
    
    headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY
    }
    
    response = requests.delete(delete_url, headers=headers)
    
    if response.status_code == 200:
        print(f"Tarefa {task_id} excluída com sucesso.")
    else:
        print(f"Erro ao excluir a tarefa {task_id}: {response.json()}")

def main():
    courses = get_courses_from_alura()
    
    if courses is None:
        return

    # Obter as tarefas existentes no ClickUp
    existing_tasks = get_existing_cards_from_clickup()
    existing_task_names = [task['name'] for task in existing_tasks]
    
    for course_progress in courses['courseProgresses']:
        # Verifica se o curso já possui um card criado
        if course_progress['name'] in existing_task_names:
            print(f"O card para o curso {course_progress['name']} já existe. Pulando criação.")
            continue  # Pula para o próximo curso
        
        # Verifica se o curso ainda não foi concluído
        if course_progress['progress'] < 100:
            create_card_in_clickup(course_progress)
        else:
            print(f"Curso concluído: {course_progress['name']}. Nenhum card será criado.")
            # Exclui a tarefa relacionada ao curso, se já existir
            if course_progress['name'] in existing_task_names:
                delete_task_in_clickup(course_progress['name'])

    for guide in courses['guides']:
        # Verifica se o guia já possui um card criado
        if guide['name'] in existing_task_names:
            print(f"O card para o guia {guide['name']} já existe. Pulando criação.")
            continue  # Pula para o próximo guia
        
        # Criar card para o guia
        create_card_in_clickup(guide)

if __name__ == "__main__":
    main()
