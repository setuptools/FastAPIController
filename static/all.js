const inputs = [];

// Получение кнопки для добавления новых полей и контейнера для полей
const inputText = document.querySelector('#input-text textarea')
const addButton = document.getElementById("add-button");
const inputFieldsContainer = document.getElementById("input-fields");
const submitButton = document.getElementById("submit-button");
// Функция для добавления нового поля
addButton.addEventListener("click", function () {
    if (inputs.length >= 100) return; 
    
    const newInput = document.createElement("input");
    newInput.type = "text";
    newInput.classList.add("input-field");
    newInput.placeholder = "Введите ссылку...";
    inputFieldsContainer.appendChild(newInput);
    inputs.push(newInput)

});

// Функция для обработки отправки данных
submitButton.addEventListener("click", async function () {
    const userIdsResponse = await fetch(`/users_ids`, { method: "GET" });

    if (!userIdsResponse.ok)
        throw new Error(`Failed to fetch user IDs: ${userIdsResponse.status}`);

    const user_ids = await userIdsResponse.text() ?? "";
    console.log("Получены user_ids:", user_ids);


    const value_text = inputText?.value?.trim() ?? '';
    const values_urls = inputs
        .map(e => e?.value?.trim() ?? '')
        .filter(Boolean)

    console.log(value_text);
    console.log(values_urls);
    console.log(user_ids);

    const response = await fetch(`/send_messages`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: value_text,
            urls: values_urls,
            user_ids: user_ids
        })
    });

    if (response.ok) {
        return true;
    } else {
        throw new Error(`HTTP error! Status: ${response.status}`);
    }
});


const textarea = document.querySelector('textarea');
const container = document.querySelector('#text-div');

textarea.addEventListener('input', () => {

    textarea.style.height = 'auto'; // Сначала сбрасываем высоту
    textarea.style.height = `${textarea.scrollHeight}px`; // Устанавливаем новую высоту на основе содержимого

    if (container.scrollHeight < 600) {
        container.style.height = `${textarea.scrollHeight + 20}px`;
    } else {
        container.style.height = `630px`;
    }
});

