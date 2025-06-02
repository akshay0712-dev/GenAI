import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import PostList from './components/PostList';
import PostDetail from './components/PostDetail';
import AddPostForm from './components/AddPostForm';
import './App.css';

const App = () => {
  const [posts, setPosts] = useState([
    { id: 1, title: 'React Fundamentals', content: 'A deep dive into the core concepts of React, including JSX, components, and state management.' },
    { id: 2, title: 'Vite Configuration', content: 'Learn how to configure Vite for optimal performance and development workflow in your React projects.' },
    { id: 3, title: 'Component Design', content: 'Best practices for designing reusable and maintainable components in React.' },
  ]);

  const handleAddPost = (newPost) => {
    setPosts([...posts, newPost]);
  };

  return (
    <Router>
      <div className="container">
        <h1>Blog App</h1>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/new">Add Post</Link>
            </li>
          </ul>
        </nav>
        <Routes>
          <Route path="/" element={<PostList posts={posts} />} />
          <Route path="/post/:id" element={<PostDetail posts={posts} />} />
          <Route path="/new" element={<AddPostForm onAddPost={handleAddPost} />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;