const serverErrorHTMLMessage = () => {
  return `
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            <strong>Sorry</strong>, <em>we cannot proceed your request right now!</em><br>
            <strong>Please try again later.</strong>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close">
            </button>
        </div>
    `;
};

const getPostCommentsChunk = async (
  url,
  postID,
  counterHTMLElement,
  errorsDiv,
  newCommentAdded = false
) => {
  try {
    const response = await fetch(url, { method: "GET" });
    if (response.ok) {
      const data = await response.json();
      if (data.commentsChunk) {
        const postCommentsDiv = document.getElementById(
          "post-comments-" + postID
        );
        if (newCommentAdded) {
          postCommentsDiv.innerHTML += `
            <div class="h6">${data.commentsChunk[0].text}</div>
          `;
        } else {
          for (let i = 0; i < data.commentsChunk.length; i++) {
            postCommentsDiv.innerHTML += `
              <div class="h6">${data.commentsChunk[i].text}</div>
            `;
          }
        }
        if (data.hasNext) {
          counterHTMLElement.innerHTML =
            Number(counterHTMLElement.innerHTML) + 1;
        } else {
          counterHTMLElement.innerHTML = 1;
        }
        return true;
      }
    } else {
      console.log("Response =>\n", response);
      errorsDiv.innerHTML += serverErrorHTMLMessage();
      return false;
    }
  } catch (error) {
    console.log("Error =>\n", error);
    return false;
  }
};

const formHandler = async (
  url,
  form,
  postID,
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
      if (titleField) {
        // It was a new post submission
        window.location.href = response.url;
      } else {
        // It was a new comment submission
        try {
          const commentsPaginationCounter = document.getElementById(
            "comments-pagination-counter-" + postID
          );
          const postCommentsURL = document.getElementById(
            "post-comments-url-" + postID
          ).innerText;
          getPostCommentsChunk(
            postCommentsURL,
            postID,
            commentsPaginationCounter,
            errorsDiv,
            true
          );
        } catch (e) {
          errorsDiv.innerHTML += serverErrorHTMLMessage();
          console.log("Error =>\n", e);
          setTimeout(() => {}, 5000);
          window.location.href = response.url;
          return false;
        }
      }
      form.elements.text.value = "";
    } else if (response.ok) {
      const data = await response.json();
      if (data.text && data.text.length > 0) {
        if (titleField) {
          titleField.classList.add("is-invalid");
        } else {
          textField.classList.add("is-invalid");
        }
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
  const form = event.target;
  const url = form.action;
  const postID = form.elements.postID.value;
  const errorsDiv = form.elements.errorsDiv;
  const textField = form.elements.text;
  const titleField = form.elements.title;
  formHandler(url, form, postID, errorsDiv, textField, titleField);
});

try {
  const commentFormsList = document.getElementsByClassName("comment-form");
  for (let i = 0; i < commentFormsList.length; i++) {
    commentFormsList[i].addEventListener("submit", (event) => {
      event.preventDefault();
      const form = event.target;
      const url = form.action;
      const postID = form.elements.postID.value;
      const errorsDiv = form.elements.errorsDiv;
      const textField = form.elements.text;
      formHandler(url, form, postID, errorsDiv, textField);
    });
  }
} catch (e) {
  console.log("Error =>\n", e);
}
