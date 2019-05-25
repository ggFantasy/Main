import React from 'react';
import icon from '../../../img/person_icon.png';
import './PlayerCard.css';
import StatsCard from "./StatsCard";


export default class PlayerCard extends React.Component {
    constructor(props) {
        super(props);

        this.state = {

        }
    }

    render() {
        let stats = this.props.player.stats;


        return (
            <div className={'PlayerCard'}>
               <div className={'icon'}>
                   <img className={'icon_img'} src={icon} />
               </div>
                <div className={'stats'}>
                    <strong>{this.props.player.summonerName}</strong>
                    <p>{this.props.player.championName}</p>
                    <StatsCard stats={stats}/>
                </div>
            </div>
        );
    }
}