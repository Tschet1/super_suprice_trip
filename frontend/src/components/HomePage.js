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

const MainButton = styled.div`
    margin: 20px;
    font-size: 28px;
    padding: 15px;
    border-radius: 5px;
    background-color: #9FA0C3;
`

const getLocation = async () => {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                return { latitude, longitude };
            },
            (error_message) => {
                console.error('An error has occured while retrieving location', error_message)
            }
        );
    } else {
        console.log('Geolocation is not enabled on this browser')
    }
}

const HomePage = props => {
    const { history } = props;

    return (
        <Home>
            <SectionDiv>
                <MainDiv>
                    <HeadingText>Super Surprise Trip</HeadingText>
                    <MainButton onClick={() => history.push("/trip")}>Find a trip now!</MainButton>
                </MainDiv>
            </SectionDiv>
            <SectionDiv>
                About
            </SectionDiv>
        </Home>
    )
}

export default withRouter(HomePage)
