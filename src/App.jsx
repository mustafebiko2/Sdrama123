import { useMemo, useState } from 'react'
import './App.css'

const genres = ['All', 'Action', 'Drama', 'Sci-Fi', 'Thriller']

const movies = [
  {
    title: 'Dune: Part Two',
    genre: 'Sci-Fi',
    rating: '8.6',
    year: '2024',
    time: '2h 46m',
    poster: 'https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg',
    backdrop: 'https://image.tmdb.org/t/p/original/xOMo8BRK7PfcJv9JCnx7s5hj0PX.jpg',
    description: 'Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.',
  },
  {
    title: 'Civil War',
    genre: 'Thriller',
    rating: '7.0',
    year: '2024',
    time: '1h 49m',
    poster: 'https://image.tmdb.org/t/p/w500/sh7Rg8Er3tFcN9BpKIPOMvALgZd.jpg',
    backdrop: 'https://image.tmdb.org/t/p/original/en3GU5uGkKaYmSyetHV4csHHiH3.jpg',
    description: 'A team of journalists races across a fractured America to reach Washington before rebel factions descend.',
  },
  {
    title: 'The Creator',
    genre: 'Action',
    rating: '7.1',
    year: '2023',
    time: '2h 14m',
    poster: 'https://image.tmdb.org/t/p/w500/vBZ0qvaRxqEhZwl6LWmruJqWE8Z.jpg',
    backdrop: 'https://image.tmdb.org/t/p/original/kcCy5YVtNGr6Gxqf0YyNSPrY3x4.jpg',
    description: 'A former special forces agent hunts a mysterious AI weapon with the power to end the war.',
  },
  {
    title: 'Past Lives',
    genre: 'Drama',
    rating: '7.8',
    year: '2023',
    time: '1h 46m',
    poster: 'https://image.tmdb.org/t/p/w500/k3waqVXSnvCZWfJYNtdamTgTtTA.jpg',
    backdrop: 'https://image.tmdb.org/t/p/original/ptz5ETMxDoRRiE69BVuIxJzyTEO.jpg',
    description: 'Two childhood friends reconnect decades later and confront the shape their lives might have taken.',
  },
  {
    title: 'Oppenheimer',
    genre: 'Drama',
    rating: '8.1',
    year: '2023',
    time: '3h 0m',
    poster: 'https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg',
    backdrop: 'https://image.tmdb.org/t/p/original/fm6KqXpk3M2HVveHwCrBSSBaO0V.jpg',
    description: 'The story of J. Robert Oppenheimer and the world-altering race to build the atomic bomb.',
  },
  {
    title: 'Furiosa',
    genre: 'Action',
    rating: '7.5',
    year: '2024',
    time: '2h 29m',
    poster: 'https://image.tmdb.org/t/p/w500/iADOJ8Zymht2JPMoy3R7xceZprc.jpg',
    backdrop: 'https://image.tmdb.org/t/p/original/wNAhuOZ3Zf84jCIlrcI6JhgmY5q.jpg',
    description: 'Young Furiosa is swept from the Green Place and must survive the brutal Wasteland.',
  },
]

function App() {
  const [selectedGenre, setSelectedGenre] = useState('All')
  const [search, setSearch] = useState('')
  const [watchlist, setWatchlist] = useState(['Dune: Part Two', 'Past Lives'])
  const featured = movies[0]

  const visibleMovies = useMemo(() => {
    return movies.filter((movie) => {
      const matchesGenre = selectedGenre === 'All' || movie.genre === selectedGenre
      const matchesSearch = movie.title.toLowerCase().includes(search.toLowerCase())
      return matchesGenre && matchesSearch
    })
  }, [search, selectedGenre])

  const watchlistMovies = movies.filter((movie) => watchlist.includes(movie.title))

  function toggleWatchlist(title) {
    setWatchlist((current) => (
      current.includes(title)
        ? current.filter((movieTitle) => movieTitle !== title)
        : [...current, title]
    ))
  }

  return (
    <main className="movie-app">
      <nav className="topbar" aria-label="Main navigation">
        <a className="brand" href="/">
          Sdrama123
        </a>
        <div className="nav-links">
          <a href="#featured">Featured</a>
          <a href="#movies">Movies</a>
          <a href="#watchlist">Watchlist</a>
        </div>
      </nav>

      <section
        className="hero"
        id="featured"
        style={{ backgroundImage: `linear-gradient(90deg, rgba(10, 12, 16, 0.94), rgba(10, 12, 16, 0.42)), url(${featured.backdrop})` }}
      >
        <div className="hero-content">
          <span className="eyebrow">Now streaming</span>
          <h1>{featured.title}</h1>
          <p>{featured.description}</p>
          <div className="hero-meta" aria-label="Movie details">
            <span>{featured.genre}</span>
            <span>{featured.year}</span>
            <span>{featured.time}</span>
            <span>{featured.rating} rating</span>
          </div>
          <div className="hero-actions">
            <a className="primary-button" href="#movies">Browse movies</a>
            <a className="secondary-button" href="#watchlist">View watchlist</a>
          </div>
        </div>
      </section>

      <section className="content-grid">
        <div className="movie-section" id="movies">
          <div className="section-header">
            <div>
              <span className="eyebrow">Library</span>
              <h2>Popular picks</h2>
            </div>
            <label className="search-field">
              <span>Search movies</span>
              <input
                type="search"
                placeholder="Search by title"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
              />
            </label>
          </div>

          <div className="genre-tabs" aria-label="Filter by genre">
            {genres.map((genre) => (
              <button
                className={genre === selectedGenre ? 'active' : ''}
                type="button"
                key={genre}
                onClick={() => setSelectedGenre(genre)}
              >
                {genre}
              </button>
            ))}
          </div>

          <div className="movie-list">
            {visibleMovies.map((movie) => (
              <article className="movie-card" key={movie.title}>
                <div className="poster-wrap">
                  <img src={movie.poster} alt={`${movie.title} poster`} />
                  <button
                    className={`love-button ${watchlist.includes(movie.title) ? 'active' : ''}`}
                    type="button"
                    aria-label={`${watchlist.includes(movie.title) ? 'Remove from' : 'Add to'} watchlist: ${movie.title}`}
                    onClick={() => toggleWatchlist(movie.title)}
                  >
                    ♥
                  </button>
                </div>
                <div className="movie-card-body">
                  <div>
                    <h3>{movie.title}</h3>
                    <p>{movie.description}</p>
                  </div>
                  <div className="movie-card-footer">
                    <span>{movie.genre}</span>
                    <strong>{movie.rating}</strong>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>

        <aside className="watchlist" id="watchlist" aria-label="Tonight watchlist">
          <span className="eyebrow">Tonight</span>
          <h2>Your watchlist</h2>
          <div className="queue">
            {watchlistMovies.length === 0 && (
              <p className="empty-watchlist">Tap a heart to save movies for later.</p>
            )}
            {watchlistMovies.map((movie, index) => (
              <div className="queue-item" key={movie.title}>
                <span>{String(index + 1).padStart(2, '0')}</span>
                <div>
                  <strong>{movie.title}</strong>
                  <p>{movie.time} · {movie.genre}</p>
                </div>
              </div>
            ))}
          </div>
          <div className="stats">
            <div>
              <strong>24</strong>
              <span>new releases</span>
            </div>
            <div>
              <strong>4K</strong>
              <span>quality</span>
            </div>
          </div>
        </aside>
      </section>
    </main>
  )
}

export default App
