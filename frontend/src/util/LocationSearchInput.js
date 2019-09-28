import React from 'react';
import PlacesAutocomplete, {
    geocodeByAddress,
    getLatLng,
} from 'react-places-autocomplete';
import styled from 'styled-components'

const ItemInSelector = styled.input`
    color: black;
    margin: 5px;
    padding: 5px;
    border-radius: 3px;
    background-color: white;
`;

const Suggestions = styled.div`
    position: absolute;
    background-color: #efefef;
    display: flex;
    flex-direction: column;
`

const Suggestion = styled.div`
    display: flex;
    border: 1px solid black;
    width: 100%;
    padding: 2px;
    font-size: 12px;
    width: 137px; 
    font-family: Roboto;
    color: black;
`;

export default class LocationInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = { address: 'Zurich, Switzerland', focused: false };
    }

    handleChange = address => {
        this.setState({ address });
    };


    render() {
        return (
            <PlacesAutocomplete
                value={this.state.address}
                onChange={this.handleChange}
                onSelect={this.handleSelect}>
                {({ getInputProps, suggestions }) => {
                    console.log(suggestions);
                    return (
                        <div>
                            <ItemInSelector {...getInputProps()} value={this.state.address} onFocus={() => this.setState({ focused: true })} onBlur={() => setTimeout(() => { this.setState({ focused: false }) }, 200)} />
                            {this.state.focused ?
                                <Suggestions>
                                    {suggestions.map(suggestion =>
                                        <Suggestion onClick={() => this.handleChange(suggestion.description)} key={suggestion.description}>{suggestion.description}</Suggestion>)}</Suggestions> : null}
                        </div>)
                }}
            </PlacesAutocomplete>
        )
    }
}

// class LocationSearchInput extends React.Component {
//     constructor(props) {
//         super(props);
//         this.state = { address: '' };
//     }

//     handleChange = address => {
//         this.setState({ address });
//     };

//     handleSelect = address => {
//         console.log(address);
//         this.setState({ address });
//         geocodeByAddress(address)
//             .then(results => getLatLng(results[0]))
//             .then(latLng => console.log('Success', latLng))
//             .catch(error => console.error('Error', error));
//     };

//     render() {
//         return (
//             <PlacesAutocomplete
//                 value={this.state.address}
//                 onChange={this.handleChange}
//                 onSelect={this.handleSelect}
//             >
//                 {({ getInputProps, suggestions, getSuggestionItemProps, loading }) => (
//                     <div>
//                         <input
//                             {...getInputProps({
//                                 placeholder: 'Search Places ...',
//                                 className: 'location-search-input',
//                             })}
//                         />
//                         <div className="autocomplete-dropdown-container">
//                             {loading && <div>Loading...</div>}
//                             {suggestions.map(suggestion => {
//                                 const className = suggestion.active
//                                     ? 'suggestion-item--active'
//                                     : 'suggestion-item';
//                                 // inline style for demonstration purpose
//                                 const style = suggestion.active
//                                     ? { backgroundColor: '#fafafa', cursor: 'pointer' }
//                                     : { backgroundColor: '#ffffff', cursor: 'pointer' };
//                                 return (
//                                     <div
//                                         {...getSuggestionItemProps(suggestion, {
//                                             className,
//                                             style,
//                                         })}
//                                     >
//                                         <span>{suggestion.description}</span>
//                                     </div>
//                                 );
//                             })}
//                         </div>
//                     </div>
//                 )}
//             </PlacesAutocomplete>
//         );
//     }
// }

// export default LocationSearchInput;