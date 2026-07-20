import React, { useState } from 'react';
import { Play, Tv, Film, Settings, Menu, Search, User } from 'lucide-react';
import './App.css';

// Premium Netflix-like UI for Movies
const MovieUI = () => (
  <div className="movie-container">
    <div className="hero-banner">
      <div className="hero-content">
        <h1 className="movie-title">The Grand Aggregator</h1>
        <p className="movie-desc">Experience the ultimate combination of all your favorite streams and playlists in one unified interface. No dead links. No duplicates.</p>
        <button className="play-btn"><Play size={24} /> Play Now</button>
      </div>
    </div>
    
    <div className="row">
      <h2>Trending Now</h2>
      <div className="carousel">
        {[1,2,3,4,5,6].map(i => (
          <div key={i} className="card">
            <div className="card-image"></div>
            <p>Movie {i}</p>
          </div>
        ))}
      </div>
    </div>
  </div>
);

// OTT Navigator-like UI for Live TV
const LiveTVUI = () => (
  <div className="tv-container">
    <div className="tv-sidebar">
      <h3>Categories</h3>
      <ul>
        <li className="active">All Channels</li>
        <li>News</li>
        <li>Sports</li>
        <li>Movies</li>
        <li>Music</li>
      </ul>
    </div>
    <div className="tv-main">
      <div className="tv-player-placeholder">
        <Tv size={64} color="#666" />
        <p>Select a channel to play</p>
      </div>
      <div className="epg-guide">
        <div className="channel-row">
          <div className="channel-info">1. BTV National</div>
          <div className="program-blocks">
            <div className="program">Morning News (08:00 - 09:00)</div>
            <div className="program active">Drama Serial (09:00 - 10:00)</div>
          </div>
        </div>
      </div>
    </div>
  </div>
);

function App() {
  const [activeTab, setActiveTab] = useState('movies');

  return (
    <div className="app-root">
      <nav className="navbar">
        <div className="nav-left">
          <span className="logo">ALL-IN-One-IPTV</span>
          <ul className="nav-links">
            <li className={activeTab === 'movies' ? 'active' : ''} onClick={() => setActiveTab('movies')}>
              <Film size={18}/> Movies
            </li>
            <li className={activeTab === 'tv' ? 'active' : ''} onClick={() => setActiveTab('tv')}>
              <Tv size={18}/> Live TV
            </li>
          </ul>
        </div>
        <div className="nav-right">
          <Search />
          <User />
        </div>
      </nav>

      <main className="main-content">
        {activeTab === 'movies' ? <MovieUI /> : <LiveTVUI />}
      </main>
    </div>
  );
}

export default App;
