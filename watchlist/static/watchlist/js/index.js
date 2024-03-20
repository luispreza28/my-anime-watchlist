// change status function
document.addEventListener('DOMContentLoaded', function () {
  const status_form = document.querySelectorAll('.status-form');
  
    status_form.forEach((status_form) => {
      status_form.addEventListener("submit", function (event) {
        event.preventDefault();

        const select_status = status_form.querySelector(".status-select").value;
        const user_id = status_form.querySelector(".user-id").value;
        const anime_id = status_form.querySelector(".anime-id").value;
        const anime_title = status_form.querySelector(".anime-title").value;

        const requestData = {
          select_status: select_status,
          user_id: user_id,
          anime_id: anime_id,
          anime_title: anime_title,
        };

        fetch(`/change-status/${user_id}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
          },
          body: JSON.stringify(requestData),
        })
          .then((response) => response.json())
          .then((data) => {
            console.log("Response:", data);
            alert(data.message);
          })
          .catch((error) => {
            console.error("Error:", error);
          });
      });
    });
})

// update current episode 
function updateEpisode(current_episode, user_id, anime_id) {
  const requestData = {
    progress: current_episode,
    user_id: user_id,
    anime_id: anime_id,
    action: "episode",
  };
  fetch(`/all-anime-watchlist/${user_id}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify(requestData),
  })
  .then(response => response.json())
  .then(data => {
    alert(data.message);
  })
  .catch(error => {
    console.error('Error:', error);
  })
}

// Update rating for anime
function updateRating(new_rating, user_id, anime_id) {
  const requestData = {
    rating: new_rating,
    user_id: user_id,
    anime_id: anime_id,
    action: "rating",
  };
  fetch(`/all-anime-watchlist/${user_id}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(requestData),
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// function to get CSRF token from cookies
function getCookie(name) {
  const cookie_value = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
  return cookie_value ? cookie_value.pop() : "";
}

// function for getting anime
function getAnime(anime_id, user_id) {
  fetch(`/get-anime/${anime_id}/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        addToWatchList(data.anime, user_id);
      } else {
        console.error("Error", data.message);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// function to add anime to watchlist
function addToWatchList(anime, user_id) {
  const requestData = {
    title: anime.title,
    description: anime.description,
    my_anime_list_url: anime.myanimelist_url,
    picture_url: anime.picture_url,
    my_anime_list_id: anime.myanimelist_id,
    genre: anime.genre,
  };
  fetch(`/add-anime/${user_id}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(requestData),
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
    })
    .then((data) => {
      alert(data.message);
    })
    .catch((error) => {
      console.error("Error:", error);
      console.log("Response:", error.response);
    });
}



// increase/decrease function
document.addEventListener('DOMContentLoaded', function (event) {
  event.preventDefault();
  
  const episode_inputs = document.querySelectorAll('.episode-input');
  const decrease_button = document.querySelectorAll('.decrease');
  const increase_button = document.querySelectorAll('.increase');
  const user_id = document.querySelector(".user-id");
  const anime_id = document.querySelectorAll('.anime-id');

  decrease_button.forEach((button, index) => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      handleDecreaseClick(episode_inputs[index],user_id.value,anime_id[index].value);
    });
  });

  increase_button.forEach((button, index) => {
    button.addEventListener('click', (event) => {
      event.preventDefault();
      handleIncreaseClick(episode_inputs[index],user_id.value,anime_id[index].value);
    });
  });

function handleIncreaseClick(episode_input, user_id,anime_id) {
  let current_episode = parseInt(episode_input.value);
  current_episode += 1;
  episode_input.value = current_episode;
  updateEpisode(episode_input.value, user_id, anime_id);
}

function handleDecreaseClick(episode_input,user_id,anime_id) {
  let current_episode = parseInt(episode_input.value);
  current_episode -= 1;
  episode_input.value = current_episode;
  updateEpisode(episode_input.value,user_id,anime_id);
}
})

// check if user clicked enter for increase/decrease function 
function checkEpisodeEnter(event, this_anime_id) {
  if (event.keyCode === 13) {
    event.preventDefault();
    console.log("Enter event");
    const episode_inputs = document.querySelectorAll('.episode-input');
    const user_id = document.querySelector(".user-id");
    const anime_id = document.querySelectorAll('.anime-id'); 
    episode_inputs.forEach((episode_input, index) => {
      if (parseInt(anime_id[index].value) === this_anime_id) {
        const current_episode = parseInt(episode_input.value);
        updateEpisode(current_episode, user_id.value, this_anime_id);
      }
    });
  }
}

function checkRatingEnter(event, this_anime_id) {
  if (event.keyCode === 13) {
    event.preventDefault();
    const rating_inputs = document.querySelectorAll(".rating-inputs");
    const user_id = document.querySelector(".user-id");
    const anime_id = document.querySelectorAll(".anime-id");
    rating_inputs.forEach((rating, index) => {
      if (parseInt(anime_id[index].value) === this_anime_id) {
        const new_rating = parseInt(rating.value);
        updateRating(new_rating, user_id.value, this_anime_id);
      }
    });
  }
}

// function for removing anime from users watchlist
function removeAnime (anime_title) {
  const requestData = {
    anime_title: anime_title
  }
  console.log(anime_title);
  fetch(`/remove-anime/${anime_title}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify(requestData),
  })
  .then(response => response.json())
  .then(data => {
    alert(data.message);
  })
  .catch(error => {
    console.error('Error:', error);
  })
}
