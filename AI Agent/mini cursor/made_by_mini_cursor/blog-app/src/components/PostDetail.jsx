import React from 'react';
import { useParams } from 'react-router-dom';

const PostDetail = ({ posts }) => {
  const { id } = useParams();
  const post = posts.find((p) => p.id === parseInt(id));

  if (!post) {
    return <div>Post not found</div>;
  }

  return (
    <div className="post-detail">
      <h2>{post.title}</h2>
      <p className="date">Published: {new Date(post.id).toLocaleDateString()}</p>
      <p>{post.content}</p>
    </div>
  );
};

export default PostDetail;