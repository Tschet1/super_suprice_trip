import React from 'react'
import { connect } from 'react-redux'
import setValue from '../util/redux/actions/Action'
import styled from 'styled-components';
import MediaQuery from "react-responsive";

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
const Trip = props => {
    console.log(props);
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
                    <div>Show options</div>
                </FlexRow>
            </MediaQuery>
        </BG>
    )
}

const mapStateToProps = state => {
    const { location, startDT, endDT, passive, wild } = state.reduxProps;
    return { location, startDT, endDT, passive, wild };
}

export default connect(mapStateToProps, { setReduxValue: setValue })(Trip);
