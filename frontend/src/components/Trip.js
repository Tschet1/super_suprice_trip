import React from 'react'
import MediaQuery from "react-responsive";

const Trip = () => {
    return (
        <div>
            <MediaQuery query="(max-aspect-ratio: 1/1)">

            </MediaQuery>
            <MediaQuery query="(min-aspect-ratio: 1/1)">
                Desktop
            </MediaQuery>
        </div>
    )
}

export default Trip
