import React, { useEffect, useState } from 'react'
import logo from './logo.svg';
import './App.css';

import Qa from './pages/qa.jsx'
import Docs from './pages/docs.jsx'

function App() {
  const [curHash, setCurHash] = useState('')

  useEffect(() => {
    const onChange = () => {
      setCurHash(window.location.hash.slice(1))
    }
    onChange()
    window.addEventListener('hashchange', onChange)
    return () => {
      window.removeEventListener('hashchange', onChange)
    }
  }, [])

  return (
    <div className="app-container" style={{ display: 'flex', flexDirection: 'column' }}>
      <header style={{ padding: '10px', textAlign: 'center', borderBottom: '1px solid #ccc' }}>
        <h1>Simple RAG</h1>
      </header>
      <div style={{ display: 'flex', flex: 1 }}>
        <nav className="sidebar" style={{ width: '20%', borderRight: '1px solid #ccc' }}>
          <ul>
            <li class="App-link">
              <a href="#/qa">Q/A</a>
            </li>
            <li class="App-link">
              <a href="#/docs">Documents</a>
            </li>
          </ul>
        </nav>
        <div className="content" style={{ width: '80%', padding: '20px' }}>
          {curHash === '/qa' && <Qa />}
          {curHash === '/docs' && <Docs />}
        </div>
      </div>
    </div>
  )
}

export default App;
