document.addEventListener("DOMContentLoaded", () => {
  const developerForm = document.getElementById("developer-form");
  const developerInfoForm = document.getElementById("developer-info-form");
  const userGenreForm = document.getElementById("user-genre-form");
  const userDataForm = document.getElementById("user-data-form");
  const bestDeveloperForm = document.getElementById("best-developer-form");
  const recommendationForm = document.getElementById("recommendation-form");
  const output = document.getElementById("output");

  developerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const developerName = document.getElementById("developer-name").value;
    const response = await fetch(`/Developer?developer=${developerName}`);
    const data = await response.json();
    output.innerHTML = JSON.stringify(data, null, 2);
  });

  developerInfoForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const developerName = document.getElementById("developer-info-name").value;
    const response = await fetch(
      `/Developer_reviews_analysis?desarrolladora=${developerName}`
    );
    const data = await response.json();
    output.innerHTML = JSON.stringify(data, null, 2);
  });

  userGenreForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const genreName = document.getElementById("genre-name").value;
    const response = await fetch(`/UserForGenre?genero=${genreName}`);
    const data = await response.json();
    output.innerHTML = JSON.stringify(data, null, 2);
  });

  userDataForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const userId = document.getElementById("user-id").value;
    const response = await fetch(`/Userdata?User_id=${userId}`);
    const data = await response.json();
    output.innerHTML = JSON.stringify(data, null, 2);
  });

  bestDeveloperForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const year = document.getElementById("year").value;
    const response = await fetch(`/Best_developer_year?año=${year}`);
    const data = await response.json();
    output.innerHTML = JSON.stringify(data, null, 2);
  });

  recommendationForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const itemName = document.getElementById("item-name").value;
    const response = await fetch(`/Recomendacion_juego`, {
      method: "POST",
      body: new URLSearchParams({
        item_name: itemName,
      }),
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
    const data = await response.json();
    output.innerHTML = JSON.stringify(data, null, 2);
  });
});
