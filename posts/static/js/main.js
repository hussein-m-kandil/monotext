const post_form_handler = async (url, form) => {
    const formData = new FormData(form);
    try {
        const response = await fetch(url, {
            "method": "POST",
            "body": formData,
        });
        if (response.redirected) {
            window.location.href = response.url;
        } else {
            const data = await response.json();
            const dataLength = data.text.length
            if (data.text && dataLength > 0) {
                errorsDiv = document.getElementById("post-form-errors");
                document.getElementById("post-text").classList.add("is-invalid");
                for (let i = 0; i < dataLength; i++) {
                    errorsDiv.innerHTML += ('<div class="text-danger">' + data.text[i] + '</div>');
                }
            }
        }
        return true;
    } catch (e) {
        console.log("Error =>\n", e);
    }
}

const post_form = document.getElementById("post-form");
post_form.addEventListener("submit", event => {
    event.preventDefault();
    post_form_handler(event.target.action, event.target);
});
