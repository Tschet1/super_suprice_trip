import React from 'react';
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom';
import HomePage from './components/HomePage';
import Trip from './components/Trip';

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={HomePage} />
        <Route exact path="/trip" component={Trip} />
        <Route path="/" component={() => <Redirect to="/" />} />
      </Switch>
    </Router>
  );
}

export default App;