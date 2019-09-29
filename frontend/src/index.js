import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { Provider } from 'react-redux';
import { createStore } from 'redux';
import reducers from './util/redux/reducers';
import * as serviceWorker from './serviceWorker';

const formatDate = (D) => {
    const S = `${D.getFullYear()}-` +
        `${D.getMonth() >= 10 ? D.getMonth() : `0${D.getMonth() + 1}`}-` +
        `${D.getDate() >= 10 ? D.getDate() : `0${D.getDate()}`}T` +
        `${D.getHours() >= 10 ? D.getHours() : `0${D.getHours()}`}:` +
        `${D.getMinutes() >= 10 ? D.getMinutes() : `0${D.getMinutes()}`}`
    // console.log(S);
    return S;
}

ReactDOM.render(
    <Provider
        store={createStore(reducers, {
            reduxProps: {
                location: "ChIJGaK-SZcLkEcRA9wf5_GNbuY",
                startDT: formatDate(new Date(Date.now())),
                endDT: formatDate(new Date(Date.now() + 60000 * 60 * 24)),
                passive: 0,
                wild: 0,
                budget: 80,
            }
        })}
    >
        <App />
    </Provider>
    , document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
