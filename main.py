async def fetch_mod(update: Update, context):
    mod_url = update.message.text  # Получаем ссылку, которую прислал пользователь
    api_url = 'https://api.steamworkshopdownloader.ru/steam.request'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'Content-Type': 'application/json',
        'Referer': 'https://yourwebsite.com'  # Укажите ваш реальный URL
    }

    try:
        # Отправляем запрос на API для получения данных о моде с заголовками
        response = requests.post(api_url, json={'url': mod_url}, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data['result'] == 0:
            await update.message.reply_text('Мод не найден или неправильная ссылка.')
        else:
            # Извлекаем информацию о моде
            mod_name = data.get('name', 'Неизвестный мод')
            mod_size = data.get('size', 'Неизвестный размер')
            download_url = data.get('url')

            # Проверяем, содержит ли ссылка рекламную часть и обрабатываем соответственно
            if download_url and 'dplgo' in download_url:
                clean_url = download_url.split('dplgo=')[-1]  # Убираем рекламную часть
                download_url = clean_url

            # Отправляем информацию о моде пользователю без ссылки на скачивание
            await update.message.reply_text(
                f"Название: {mod_name}\nРазмер: {mod_size}\nЗагружаю файл..."
            )

            # Загружаем файл и отправляем пользователю
            if download_url:
                file_response = requests.get(download_url)
                file_response.raise_for_status()

                # Используем фиксированное имя файла
                filename = "MOD.zip"  # Имя файла, который будет отправлен

                # Отправляем файл пользователю с указанным именем
                await context.bot.send_document(
                    chat_id=update.effective_chat.id,
                    document=file_response.content,
                    filename=filename
                )

    except requests.RequestException as e:
        await update.message.reply_text(f'Ошибка при получении данных: {e}')
