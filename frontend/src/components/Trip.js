import React from 'react'
import { connect } from 'react-redux'
import setValue from '../util/redux/actions/Action'
import styled from 'styled-components';
import MediaQuery from "react-responsive";
import Axios from 'axios';

const BG = styled.div`
    height: calc(100vh - 40px);
    overflow: auto;
    background-color: #AED9E0
    color: #ffffff
    padding: 20px;
    flex: 1;
`;

const FlexRow = styled.div`
    flex: 1;
    height: calc(100% - 40px);
    display: flex;
    flex-flow: row nowrap;
    justify-content: space-between;
`

const FlexCol = styled.div`
    height: 100%;
    display: flex;
    flex-flow: column nowrap;
    justify-content: flex-start;
`

const OptionsCol = styled.div`
    display: flex;
    flex-flow: column nowrap;
    width: 300px;
    padding: 20px;
    border-radius: 10px;
    height: 100%;
    background-color: #9FA0C3;
    overflow: auto;
`;

const MyOptions = props => {
    console.log(props);
    return (
        <OptionsCol>
            <h1>Travel Options</h1>
            {props.ops.map((op, index) => { const n = `${op.name}!${index}`; return <p key={n}>{op.name}</p> })}
        </OptionsCol>
    );
}

class Trip extends React.Component {
    constructor(props) {
        super(props);
        this.state = { options: [] }
    }

    getOptions = async () => {
        const { location, startDT, endDT, passive, wild, budget } = this.props;
        Axios.get(`http://206.189.50.95:8000/api/surprize?location=${location}&startDT=${startDT}&endDT=${endDT}&social_score=${wild}&activity_score=${passive}&budget=${budget}`)
            .then(val => {
                console.log(val);
                if (val.data.success) {
                    this.setState({ options: val.data.results });
                }
            }
            );
    }

    componentDidMount = async () => {
        await this.getOptions();
    }

    async handleChange(e, prop) {
        this.props.setReduxValue({ prop, value: e.target.value });
        this.getOptions();
    }

    render() {
        console.log(this.props);
        return (
            <BG>
                <FlexRow>
                    <FlexCol>
                        <h1>Preferences</h1>
                        <div>Active <input onChange={(e) => this.handleChange(e, "passive")} type="range" name="points" min="1" max="100" /> Passive</div>
                        <div>Museum <input onChange={(e) => this.handleChange(e, "wild")} type="range" name="points" min="1" max="100" /> Concert/Party</div>
                        <div>Budget <input onChange={(e) => { this.props.setReduxValue({ prop: "budget", value: e.target.value }) }} type="number" value={this.props.budget} /></div>
                    </FlexCol>
                    <MyOptions ops={this.state.options} />
                </FlexRow>
            </BG>
        )
    }
}

const mapStateToProps = state => {
    const { location, startDT, endDT, passive, wild, budget } = state.reduxProps;
    return { location, startDT, endDT, passive, wild, budget };
}

export default connect(mapStateToProps, { setReduxValue: setValue })(Trip);
