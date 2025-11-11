let page = 1;
const limit = 6;
const container = document.getElementById("movie-container");

// Busca os filmes com filtros e paginação
async function fetchMovies() {
    const search = document.getElementById("search")?.value || "";
    const year = document.getElementById("year")?.value || "All";
    const sort_by = document.getElementById("sort")?.value || "title";
    const order = document.getElementById("order")?.value || "asc";

    const url = `/movies/?search=${encodeURIComponent(search)}&year=${encodeURIComponent(year)}&sort_by=${encodeURIComponent(sort_by)}&order=${encodeURIComponent(order)}&page=${page}&limit=${limit}`;

    try {
        const res = await fetch(url);
        if (!res.ok) {
            container.innerHTML = "<p>Nenhum filme encontrado.</p>";
            return;
        }
        const movies = await res.json();
        renderMovies(movies);
    } catch (err) {
        container.innerHTML = "<p>Erro ao carregar filmes.</p>";
        console.error(err);
    }
}

// Render de filmes no catálogo
function renderMovies(movies) {
    container.innerHTML = "";
    if (!movies.length) {
        container.innerHTML = "<p>Nenhum filme encontrado.</p>";
        return;
    }
    movies.forEach(movie => {
        const card = document.createElement("div");
        card.className = "movie-card";
        card.innerHTML = `
            <img src="${movie.poster || 'https://via.placeholder.com/300x450?text=Sem+Poster'}" alt="${movie.title}">
            <h3>${movie.title}</h3>
            <p>Ano: ${movie.year}</p>
            <p>IMDb: ${movie.imdb_rating}</p>
        `;
        container.appendChild(card);
    });
}

// Carrega anos para filtro
async function loadYears() {
    try {
        const res = await fetch("/movies/years");
        const years = await res.json();
        const yearSelect = document.getElementById("year");
        yearSelect.innerHTML = `<option value="All">Todos os anos</option>`;
        years.forEach(y => {
            const opt = document.createElement("option");
            opt.value = y;
            opt.textContent = y;
            yearSelect.appendChild(opt);
        });
    } catch (err) {
        console.error("Erro ao carregar anos", err);
    }
}

// Cria os eventos de filtros e refresh
document.getElementById("search").addEventListener("input", () => { page = 1; fetchMovies(); });
document.getElementById("year").addEventListener("change", () => { page = 1; fetchMovies(); });
document.getElementById("sort").addEventListener("change", () => { page = 1; fetchMovies(); });
document.getElementById("order").addEventListener("change", () => { page = 1; fetchMovies(); });
document.getElementById("refresh").addEventListener("click", () => { page = 1; fetchMovies(); });

// Paginação
document.getElementById("prev").addEventListener("click", () => { if(page>1){ page--; fetchMovies(); } });
document.getElementById("next").addEventListener("click", () => { page++; fetchMovies(); });

// Inicialização
loadYears();
fetchMovies();
