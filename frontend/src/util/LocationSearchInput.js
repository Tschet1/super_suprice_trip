import React from 'react';
import PlacesAutocomplete from 'react-places-autocomplete';
import { connect } from 'react-redux'
import setValue from './redux/actions/Action'
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

class LocationInput extends React.Component {
    constructor(props) {
        super(props);
        this.state = { address: 'Zürich, Switzerland', focused: false };
    }

    handleChange = address => {
        this.setState({ address });
        this.props.setReduxValue({ prop: 'location', value: address });
    }

    render() {
        return (
            <PlacesAutocomplete
                value={this.state.address}
                onChange={this.handleChange}
                onSelect={this.handleSelect}>
                {({ getInputProps, suggestions }) => {
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

export default connect(null, { setReduxValue: setValue })(LocationInput);