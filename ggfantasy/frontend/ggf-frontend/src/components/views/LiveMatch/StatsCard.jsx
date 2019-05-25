import React from 'react';
import './StatsCard.css';

const KEYS = [
    'kills',
    'deaths',
    'assists',
    'doubleKills',
    'tripleKills',
    'quadraKills',
    'pentaKills',
    'mk'
];


export default class StatsCard extends React.Component {
    constructor(props) {
        super(props);
    }

    renderStat(key, value) {
        let displayed_value = value ? value:0;
        return (
            <div className={'StatsCard'}>
                <strong>{key}:</strong> {displayed_value}
            </div>
        )
    }

    render() {
        const stats = [];
        KEYS.forEach(key => {
            stats.push(this.renderStat(key, this.props.stats[key]));
        });
        return (
            <div>
                {stats}
            </div>
        );
    }
}
