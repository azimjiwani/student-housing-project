import React from 'react';
import { View,Text } from 'react-native';
import MapView, {Marker, PROVIDER_GOOGLE} from 'react-native-maps';

const CustomMarker = (props) => {

    const {coordinate,price,onPress,isSelected} = props;

    return (
        <Marker coordinate={coordinate} onPress={onPress}>
            <View style={{
                backgroundColor: isSelected ? "black" : "white",
                padding:5,
                borderRadius:20,
                borderColour:'grey',
                borderWidth:1
                }}>
                    <Text style={{color: isSelected ? "white" : "black", fontWeight: "bold"}}>${price}</Text>
            </View>
        </Marker>
    );
}

export default CustomMarker;