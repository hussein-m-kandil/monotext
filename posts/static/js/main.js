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

const currentPageFullPath = document.getElementById("current-page-full-path");
const CURRENT_PAGE_URL = currentPageFullPath.innerText;
currentPageFullPath.remove();
const createNewComment = (commentObject, postID) => {
  return `
    <div class="comment-on-post-${postID} m-3 border round p-2 shadow-sm">
      <div class="d-flex justify-content-between">
        <span class="align-self-start h6 text-start">
          <a href="${
            CURRENT_PAGE_URL + "profile/" + commentObject.ownerName
          }" class="text-decoration-none link-secondary">
            <strong><em>${commentObject.ownerName}</em></strong>
          </a>
        </span>
        <span class="align-self-end h6 text-secondary text-end">
          <em>${commentObject.createdAt}</em>
        </span>
      </div>
      <hr class="mt-1 text-secondary">
      <div class="h6 text-center">${commentObject.text}</div>
    </div>
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

const postCommentsPopulation = async (postID, commentsLink) => {
  await commentsLink.addEventListener("click", (event) => {
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
            data.commentsChunk[i],
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
        // Although, it was a new comment submission,
        // i won't update the comments with the new comment interactively :D
        window.location.href = response.url;
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
  const errorsDiv = form.children.errorsDiv;
  const textField = form.elements.text;
  textField.addEventListener("input", (event) => {
    event.target.classList.remove("is-invalid");
  });
  const titleField = form.elements.title;
  titleField.addEventListener("input", (event) => {
    event.target.classList.remove("is-invalid");
  });
  formHandler(url, form, errorsDiv, textField, titleField);
});

const postCommentsDiv = document.getElementsByClassName("post-comments-div");
for (let i = 0; i < postCommentsDiv?.length; i++) {
  const postID = postCommentsDiv[i].id.match(/\d+/)[0];
  const postMoreCommentsLink = document.getElementById(
    "post-more-comments-link-" + postID
  );
  postCommentsPopulation(postID, postMoreCommentsLink).then((_) => {
    postMoreCommentsLink.click();
  });
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
    formHandler(url, form, errorsDiv, textField);
  });
}

// Post likes logic
const CSRFTokenInput = document.getElementsByName("csrfmiddlewaretoken")[0];
if (CSRFTokenInput) {
  const postLikesCountList =
    document.getElementsByClassName("post-likes-count");
  for (let i = 0; i < postLikesCountList?.length; i++) {
    const postID = postLikesCountList[i]?.id.match(/\d+/)[0];
    const postLikesCountSpan = document.getElementById(
      "post-likes-count-number-" + postID
    );
    const likeButton = document.getElementById("like-btn-" + postID);
    const dislikeButton = document.getElementById("dislike-btn-" + postID);
    likeButton?.addEventListener("click", (event) => {
      event.preventDefault();
      let formData = new FormData();
      formData.append("csrfmiddlewaretoken", CSRFTokenInput.value);
      fetch(likeButton.value, {
        method: "POST",
        body: formData,
      }).then((response) => {
        response.json().then((jsonResponse) => {
          postLikesCountSpan.innerText = jsonResponse.likes;
          likeButton.style.display = "none";
          dislikeButton.style.display = "block";
        });
      });
    });
    dislikeButton?.addEventListener("click", (event) => {
      event.preventDefault();
      let formData = new FormData();
      formData.append("csrfmiddlewaretoken", CSRFTokenInput.value);
      fetch(dislikeButton.value, {
        method: "POST",
        body: formData,
      }).then((response) => {
        response.json().then((jsonResponse) => {
          postLikesCountSpan.innerText = jsonResponse.likes;
          dislikeButton.style.display = "none";
          likeButton.style.display = "block";
        });
      });
    });
  }
}
