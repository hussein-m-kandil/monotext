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

const createNewComment = (commentText, postID) => {
  return `
    <div class="comment-on-post-${postID} h6">${commentText}</div>
  `;
};

const getPostCommentsChunk = async (url) => {
  try {
    const response = await fetch(url, {
      method: "GET",
    });
    if (response.ok) {
      const data = await response.json();
      return data;
    } else {
      console.log("Response =>\n", response);
      return false;
    }
  } catch (error) {
    console.log("Error =>\n", error);
    return false;
  }
};

const postCommentsPopulation = (postID, commentsLink) => {
  commentsLink.addEventListener("click", (event) => {
    event.preventDefault();
    const lessCommentsLinkText = "... Less comments";
    const postMoreCommentsLink = event.target;
    const postCommentsDiv = document.getElementById("post-comments-" + postID);
    const commentsPageCounter = document.getElementById(
      "comments-page-counter-" + postID
    );
    const postCommentsURL = document.getElementById(
      "post-comments-url-" + postID
    ).innerText;
    const url = postCommentsURL + "?page=" + commentsPageCounter.innerText;
    getPostCommentsChunk(url).then((data) => {
      if (data.commentsCount > 0) {
        if (postMoreCommentsLink.innerText == lessCommentsLinkText) {
          postCommentsDiv.innerHTML = "";
          postMoreCommentsLink.innerText = "More comments...";
          postCommentsDiv.appendChild(postMoreCommentsLink);
        }
        postCommentsDiv.removeChild(postMoreCommentsLink);
        for (let i = 0; i < data.commentsChunk.length; i++) {
          postCommentsDiv.innerHTML += createNewComment(
            data.commentsChunk[i].text,
            postID
          );
        }
        postCommentsDiv.appendChild(postMoreCommentsLink);
        if (data.hasNext) {
          commentsPageCounter.innerText =
            Number(commentsPageCounter.innerText) + 1;
          postMoreCommentsLink.style.display = "block";
        } else {
          commentsPageCounter.innerText = 1;
          if (data.commentsCount > 2) {
            postMoreCommentsLink.innerText = lessCommentsLinkText;
          } else {
            postMoreCommentsLink.style.display = "none";
          }
        }
      }
    });
  });
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
          // Logic for getting the added new comment.
          const postCommentsDiv = document.getElementById(
            "post-comments-" + postID
          );
          postCommentsDiv.innerHTML =
            createNewComment(textField.value, postID) +
            postCommentsDiv.innerHTML;
          const postMoreCommentsLink = document.getElementById(
            "post-more-comments-link-" + postID
          );
          postCommentsPopulation(postID, postMoreCommentsLink);
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
postForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  const form = event.target;
  const url = form.action;
  const postID = form.elements.postID.value;
  const errorsDiv = form.children.errorsDiv;
  const textField = form.elements.text;
  textField.addEventListener("input", (event) => {
    event.target.classList.remove("is-invalid");
  });
  const titleField = form.elements.title;
  titleField.addEventListener("input", (event) => {
    event.target.classList.remove("is-invalid");
  });
  formHandler(url, form, postID, errorsDiv, textField, titleField);
});

const postCommentsDiv = document.getElementsByClassName("post-comments-div");
for (let i = 0; i < postCommentsDiv?.length; i++) {
  const postID = postCommentsDiv[i].id.match(/\d+/)[0];
  const postMoreCommentsLink = document.getElementById(
    "post-more-comments-link-" + postID
  );
  postCommentsPopulation(postID, postMoreCommentsLink);
  postMoreCommentsLink.click();
}

const commentFormsList = document.getElementsByClassName("comment-form");
for (let i = 0; i < commentFormsList?.length; i++) {
  commentFormsList[i].addEventListener("submit", (event) => {
    event.preventDefault();
    const form = event.target;
    const url = form.action;
    const textField = form.elements.text;
    textField.addEventListener("input", (event) => {
      event.target.classList.remove("is-invalid");
    });
    const errorsDiv = form.children.errorsDiv;
    const postID = form.elements.postID.value;
    formHandler(url, form, postID, errorsDiv, textField);
  });
}
