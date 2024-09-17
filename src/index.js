import React from 'react';
import ReactDOM from 'react-dom';

import './index.css';
import App from './App';
import SearchScreen from './screens/SearchScreen';
import SelectionScreen from './screens/SelectionScreen';

import registerServiceWorker from './registerServiceWorker';
import reportWebVitals from './reportWebVitals';

import { eel } from './eel';
eel.set_host("ws://localhost:8888");

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <App />
);

registerServiceWorker();
reportWebVitals();