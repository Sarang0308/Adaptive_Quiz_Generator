// --- File: src/components/RoleSelector.jsx ---
import React from 'react';
import { Link } from 'react-router-dom';

function RoleSelector() {
  return (
    <div>
      <h1>Choose Role</h1>
      <Link to="/admin"><button>Admin</button></Link>
      <Link to="/student"><button>Student</button></Link>
    </div>
  );
}

export default RoleSelector;
