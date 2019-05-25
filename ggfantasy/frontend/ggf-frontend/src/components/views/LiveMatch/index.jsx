import React from 'react';
import Websocket from 'react-websocket';
import PlayerCard from "./PlayerCard";



class LiveMatch extends React.Component {
    constructor(props) {
    super(props);

    this.state = {
      message: 'Waiting for another player...',
        teams: "Empty",
        players: {}
    };

    this.handleData = this.handleData.bind(this);
    }

    loadPlayers(teamOne, teamTwo) {
        let players = {};
        Object.values(teamOne).forEach(player => {
            player['stats'] = {};
            players[player.participantId] = player
        });
        Object.values(teamTwo).forEach(player => {
            player['stats'] = {};
            players[player.participantId] = player
        });
        console.log(players);
        this.setState({players})
    }

    playersHeader(players) {
        if (!players) return;
        let playerList = [];
        Object.values(players).forEach(player => {
            playerList.push(
                // Should now feed into a presentational component - PlayerCards
                <PlayerCard player={player}/>
            )
        })
        return (
            <div>
                {playerList}
            </div>
        );
    }

    updatePlayers(data) {
        // playerStats {"2002890034": {"playerStats": {"2": {}, "3": {}, "4": {}, "5": {}, "7": {}, "9": {}, "10": {}}}}

        // Copies players object from state
        const newPlayers = { ...this.state.players };

        // removes timestamp key and deconstructs playerStats
        const { playerStats } = Object.values(data)[0];

        Object.keys(playerStats).forEach((playerId) => {
            let pid = parseInt(playerId)
            const player = newPlayers[pid]

            newPlayers[pid] = {
                ...player,
                stats: { ...player.stats, ...playerStats[playerId]}
            }
        });

        this.setState({ players: newPlayers })
    }


    handleData(data) {
        let parsed = JSON.parse(data);
        if (parsed.gameId) {
            console.log("Loading Players");
            this.loadPlayers(parsed.primaryTeam, parsed.secondaryTeam)
        }
        else {
            console.log("Updating Player Stats");
            this.updatePlayers(Object.values(parsed));
        }
      let result = data;
      console.log(result);
      this.setState({message: result});
    }

    render() {
      return (
        <div>
          Count: <strong>{this.state.message}</strong>
            <div>Players: {this.playersHeader(this.state.players)}</div>

          <Websocket url='ws://localhost:7777'
              onMessage={this.handleData}/>
        </div>
      );
    }
}

export default LiveMatch;