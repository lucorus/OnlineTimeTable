def generate_main_page(schedule_data: list) -> str:
    html_content = """
       <!DOCTYPE html>
       <html lang="ru">
       <head>
           <meta charset="UTF-8">
           <meta name="viewport" content="width=device-width, initial-scale=1.0">
           <title>Расписание</title>
           <style>
               body {
                   background-color: #1e1e1e;
                   color: #e0e0e0;
                   font-family: Arial, sans-serif;
                   margin: 0;
                   padding: 0;
                   overflow: hidden;
               }
               h1 {
                   text-align: center;
                   padding: 20px;
                   background-color: #333;
               }
               .schedule-container {
                   display: flex;
                   overflow-x: auto;
                   scroll-behavior: smooth;
                   padding: 20px 0;
                   gap: 20px;
               }
               .class-schedule {
                   min-width: 300px;
                   max-width: 300px;
                   border: 1px solid #444;
                   padding: 20px;
                   box-sizing: border-box;
                   background-color: #2e2e2e;
                   border-radius: 8px;
                   transition: transform 0.3s ease, background-color 0.3s ease;
               }
               .class-schedule h3 {
                   margin-top: 0;
                   border-bottom: 2px solid #555;
                   padding-bottom: 10px;
               }
               .lesson {
                   margin: 10px 0;
                   padding: 10px;
                   border-radius: 5px;
                   background-color: #3e3e3e;
                   transition: background-color 0.3s ease;
               }
               .lesson:hover {
                   background-color: #4a4a4a;
               }
               .date-header {
                   font-weight: bold;
                   margin-top: 15px;
                   border-bottom: 1px solid #555;
                   padding-bottom: 5px;
               }
               .navigation {
                   position: fixed;
                   top: 50%;
                   width: 100%;
                   display: flex;
                   justify-content: space-between;
                   pointer-events: none;
               }
               .nav-button {
                   background-color: #333;
                   border: none;
                   color: #e0e0e0;
                   padding: 10px;
                   cursor: pointer;
                   pointer-events: auto;
                   border-radius: 5px;
                   transition: background-color 0.3s ease;
               }
               .nav-button:hover {
                   background-color: #4a4a4a;
               }
           </style>
       </head>
       <body>
           <h1>Расписание</h1>
           <div class="navigation">
               <button class="nav-button" id="prev-button">&#9664;</button>
               <button class="nav-button" id="next-button">&#9654;</button>
           </div>
           <div class="schedule-container" id="schedule-container">
       """

    # Группировка данных по классам и датам
    class_schedule_map = {}
    for entry in schedule_data:
        class_name = entry[6]  # Индекс для класса
        date = entry[8]  # Индекс для даты
        if class_name not in class_schedule_map:
            class_schedule_map[class_name] = {}
        if date not in class_schedule_map[class_name]:
            class_schedule_map[class_name][date] = []
        class_schedule_map[class_name][date].append({
            'time': entry[2],
            'room': entry[4],
            'subject': entry[10]
        })

    # Генерация HTML для каждого класса и даты
    for class_name, dates in class_schedule_map.items():
        html_content += f"""
           <div class="class-schedule">
               <h3>{class_name}</h3>
           """
        for date, schedule in dates.items():
            html_content += f"""
               <div class="date-header">{date}</div>
               """
            for entry in schedule:
                html_content += f"""
                   <div class="lesson">
                       {entry['time']} {entry['subject']} ({entry['room']})
                   </div>
                   """
        html_content += "</div>"

    html_content += """
           </div>
           <script>
               document.addEventListener('DOMContentLoaded', function() {
                   const prevButton = document.getElementById('prev-button');
                   const nextButton = document.getElementById('next-button');
                   const scheduleContainer = document.getElementById('schedule-container');
                   let scrollAmount = 0;

                   prevButton.addEventListener('click', () => {
                       scrollAmount = Math.max(scrollAmount - 300, 0);
                       scheduleContainer.scrollTo({ left: scrollAmount, behavior: 'smooth' });
                   });

                   nextButton.addEventListener('click', () => {
                       scrollAmount = Math.min(scrollAmount + 300, scheduleContainer.scrollWidth - window.innerWidth);
                       scheduleContainer.scrollTo({ left: scrollAmount, behavior: 'smooth' });
                   });
               });
           </script>
       </body>
       </html>
       """
    return html_content
