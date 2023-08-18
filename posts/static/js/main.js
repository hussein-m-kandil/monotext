const serverErrorHTMLMessage = () => {
  return `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            <strong>Sorry</strong>, <em>we cannot publish your post right now!</em><br>
            <strong>Please try again later.</strong>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">
            </button>
        </div>
    `;
};

const formHandler = async (
  url,
  form,
  errorsDiv,
  textField,
  titleField = false
) => {
  const formData = new FormData(form);
  try {
    const response = await fetch(url, {
      method: "POST",
      body: formData,
    });
    if (response.redirected) {
      window.location.href = response.url;
    } else if (response.ok) {
      const data = await response.json();
      if (data.text && data.text.length > 0) {
        textField.classList.add("is-invalid");
        for (let i = 0; i < data.text.length; i++) {
          errorsDiv.innerHTML += `
                        <div class="alert alert-danger alert-dismissible fade show" role="alert">
                            ${data.text[i]}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">
                            </button>
                        </div>
                    `;
        }
      }
      if (titleField && data.title && data.title.length > 0) {
        titleField.classList.add("is-invalid");
        for (let i = 0; i < data.text.length; i++) {
          errorsDiv.innerHTML += `
                        <div class="alert alert-danger alert-dismissible fade show" role="alert">
                            ${data.text[i]}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">
                            </button>
                        </div>
                    `;
        }
      }
    } else {
      console.log("Response =>\n", response);
      errorsDiv.innerHTML += serverErrorHTMLMessage();
      return false;
    }
    return true;
  } catch (e) {
    console.log("Error =>\n", e);
    errorsDiv.innerHTML += serverErrorHTMLMessage();
    return false;
  }
};

const postForm = document.getElementById("post-form");
postForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const errorsDiv = document.getElementById("post-form-errors");
  const textField = document.getElementById("post-text");
  const titleField = document.getElementById("post-title");
  formHandler(
    event.target.action,
    event.target,
    errorsDiv,
    textField,
    titleField
  );
});

const commentForm = document.getElementById("comment-form");
commentForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const errorsDiv = document.getElementById("comment-form-errors");
  const textField = document.getElementById("comment-text");
  formHandler(event.target.action, event.target, errorsDiv, textField);
});
