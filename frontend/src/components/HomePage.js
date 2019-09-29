import React from 'react'
import { withRouter } from 'react-router-dom'
import { connect } from 'react-redux'
import styled from 'styled-components'
import setValue from '../util/redux/actions/Action'
import LocationInput from '../util/LocationSearchInput';

const Home = styled.div`
    background-color: #AED9E0
    color: #ffffff
`;

const SectionDiv = styled.div`
    height: 100vh;
    display: flex;
`;

const MainDiv = styled.div`
    display: flex;
    font-family: 'Indie Flower', cursive;
    justify-content: center;
    align-items: center;
    margin: 20px;
    flex: 1;
    flex-flow: column nowrap;
`

const HeadingText = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    font-size: calc(12vw - 15px);
`

const SelectorDiv = styled.div`
    margin: 20px;
    width: calc(100% - 40px);
    display: flex;
    flex-flow: row wrap;
    font-size: 28px;
    padding: 15px;
    border-radius: 5px;
    background-color: #9FA0C3;
    justify-content: center;
    align-items: center;
`

const ItemInSelector = styled.input`
    color: black;
    margin: 5px;
    padding: 5px;
    border-radius: 3px;
    background-color: white;
`;

const HomePage = props => {
    const { history, startDT, endDT, setReduxValue } = props;
    return (
        <Home>
            <SectionDiv>
                <MainDiv>
                    <HeadingText>Super Surprise Trip</HeadingText>
                    <SelectorDiv>
                        <LocationInput />
                        <ItemInSelector type="datetime-local" value={startDT} onChange={(e) => setReduxValue({ prop: 'startDT', value: e.target.value })}></ItemInSelector>
                        <ItemInSelector type="datetime-local" value={endDT} onChange={(e) => setReduxValue({ prop: 'endDT', value: e.target.value })}></ItemInSelector>
                        <ItemInSelector type="submit" onClick={() => history.push('/trip')} value="Find my trip"></ItemInSelector>
                    </SelectorDiv>
                </MainDiv>
            </SectionDiv>
        </Home>
    )
}

const mapStateToProps = (state) => {
    const { startDT, endDT } = state.reduxProps;
    return { startDT, endDT };
}

export default connect(mapStateToProps, { setReduxValue: setValue })(withRouter(HomePage));
