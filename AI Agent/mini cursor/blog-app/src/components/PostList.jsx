import React from 'react';
import { Link } from 'react-router-dom';

const PostList = ({ posts }) => {
  return (
    <div className="posts">
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <div className="card">
              <Link to={`/post/${post.id}`}>{post.title}</Link>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PostList;