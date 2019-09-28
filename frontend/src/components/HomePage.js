import React from 'react'
import { withRouter } from 'react-router-dom'
import styled from 'styled-components'

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

const formatDate = (D) => {
    const S = `${D.getFullYear()}-` +
        `${D.getMonth() >= 10 ? D.getMonth() : `0${D.getMonth()}`}-` +
        `${D.getDate() >= 10 ? D.getDate() : `0${D.getDate()}`}T` +
        `${D.getHours() >= 10 ? D.getHours() : `0${D.getHours()}`}:` +
        `${D.getMinutes() >= 10 ? D.getMinutes() : `0${D.getMinutes()}`}`
    // console.log(S);
    return S;
}

const HomePage = props => {
    // const { history } = props;
    return (
        <Home>
            <SectionDiv>
                <MainDiv>
                    <HeadingText>Super Surprise Trip</HeadingText>
                    <SelectorDiv>
                        <ItemInSelector type="text" defaultValue="Location"></ItemInSelector>
                        <ItemInSelector type="datetime-local" defaultValue={formatDate(new Date())} onChange={(e) => console.log(e.target.value)}></ItemInSelector>
                        <ItemInSelector type="datetime-local" defaultValue={formatDate(new Date(Date.now() + 60000 * 60 * 24))} onChange={(e) => console.log(e.target.value)}></ItemInSelector>
                        <ItemInSelector type="submit" value="Find my trip"></ItemInSelector>
                    </SelectorDiv>
                </MainDiv>
            </SectionDiv>
        </Home>
    )
}

export default withRouter(HomePage)
