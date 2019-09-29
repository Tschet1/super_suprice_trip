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
    justify-content: space-between;
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
    return (<OptionsCol>
        {props.ops.map(op => <p key={op.name}>{op.name}</p>)}
    </OptionsCol>);
}

class Trip extends React.Component {
    constructor(props) {
        super(props);
        this.state = { options: [] }
    }

    getOptions = async () => {
        Axios.get(`http://206.189.50.95:8000/api/surprize?lat=47.390499&long=8.515806&departure=${this.props.startDT}`)
            .then(val => this.setState({ options: val.data.results }));
    }

    componentDidMount = async () => {
        await this.getOptions();
    }

    render() {

        return (
            <BG>
                <MediaQuery query="(max-aspect-ratio: 1/1)">
                    <FlexCol>
                        <div>Preferences</div>
                        <div>Show options</div>
                    </FlexCol>
                </MediaQuery>
                <MediaQuery query="(min-aspect-ratio: 1/1)">
                    <FlexRow>
                        <div>Preferences</div>
                        <MyOptions ops={this.state.options} />
                    </FlexRow>
                </MediaQuery>
            </BG>
        )
    }
}

const mapStateToProps = state => {
    const { location, startDT, endDT, passive, wild } = state.reduxProps;
    return { location, startDT, endDT, passive, wild };
}

export default connect(mapStateToProps, { setReduxValue: setValue })(Trip);
