import React, { useState } from 'react';
import { View, Image, StyleSheet, useColorScheme, Platform, Button, ActionSheetIOS, TouchableOpacity, Alert } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { IconSymbol } from '@/components/ui/IconSymbol';
// import {/* backend hook */} from '@/hooks/imageEnhancer';
import * as ImagePicker from 'expo-image-picker';

export default function EnhanceScreen() {

    const [ selectedImage, setSelectedImage ] = useState<string | null>(null);
    const [ enhancedImage, setEnhancedImage ] = useState<string | null>(null);
    const [ loading, setLoading ] = useState(false);
    const [ model, setModel ] = useState('');
    const [ modelLabel, setModelLabel ] = useState('Select a model');

    const colorScheme = useColorScheme();
    const isDark = colorScheme === 'dark';

    {/* Model Selection Functionality */}
    const openModelPicker = () => {
        const options = ['Default model', 'Anime model', 'Traditional', 'Cancel'];
        const values = ['default', 'anime', 'traditional'];

        ActionSheetIOS.showActionSheetWithOptions(
            {
                options,
                cancelButtonIndex: options.length - 1,
            },
            (buttonIndex) => {
                if (buttonIndex === options.length - 1) return; // Cancel button
                setModel(values[buttonIndex]);
                setModelLabel(options[buttonIndex]);
            }
        );
    };


    {/* Image Picker Functionality */}
    const pickImage = async () => {
        try {
            const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
            if (status !== 'granted') {
                alert('Sorry, we need camera roll permissions to make this work!');
                return;
            }
            
            // Launch the image picker
            const result = await ImagePicker.launchImageLibraryAsync({
                mediaTypes: ImagePicker.MediaTypeOptions.Images,
                allowsEditing: true,
                aspect: [4, 3],
                quality: 1,
            });

            if (!result.canceled && result.assets.length > 0) {
                setSelectedImage(result.assets[0].uri);
                setEnhancedImage(null); // Reset enhanced image when a new image is selected
            }
        } catch (error) {
            console.error('Error picking image:', error);
            alert('Error picking image. Please try again.');
        }
    };

    {/* Enhance Image Functionality */}
    const enhanceImage = async () => {
        if (!selectedImage) {
            alert('Please select an image first!');
            return;
        }

        if (!model) {
            alert('Please select a model first!');
            return;
        }

        try {
            setLoading(true);
            // Call the backend API to enhance the image
            // const response = await enhanceImageAPI(selecterImage, model); // Replace with actual API call
            // setEnhancedImage(response.enhancedImage); // Set the enhanced image from the API response
            setEnhancedImage(selectedImage); // Placeholder for enhanced image
        } catch (error) {
            console.error('Error enhancing image:', error);
            alert('Error enhancing image. Please try again.');
        } finally {
            setLoading(false);
        }
    };


    return (
        <ThemedView style={styles.container}>
            <ParallaxScrollView
                headerBackgroundColor={{ light: '#fef3c7', dark: '#4b3c0a' }}
                headerImage={
                <IconSymbol
                    size={300}
                    color="#facc15"
                    name="wand.and.stars"
                    style={styles.headerImage}
                    />
                }
            >
                <ThemedView style={styles.titleContainer}>
                    <ThemedText type="title">Enhance</ThemedText>
                </ThemedView>

                <ThemedText>Select a model and upload an image to enhance it.</ThemedText>
                
                {/* Model Selection */}
                <View style={styles.section}>
                    <ThemedText style={styles.label}>Model:</ThemedText>
                    <TouchableOpacity style={[
                        styles.modelField,
                        { backgroundColor: isDark ? '#4b3c0a' : '#fef3c7' },
                    ]} 
                        onPress={openModelPicker}
                    >
                        <ThemedText
                            style={[
                                styles.modelText,
                                { color: isDark ? '#facc15' : '#4b3c0a' },
                            ]}>
                            {modelLabel}
                        </ThemedText>
                    </TouchableOpacity>
                </View>

                {/* Image Upload Button */}
                <View style={styles.uploadingContainer}>
                    <Button title="Upload a Picture" onPress={pickImage} color={colorScheme === 'dark' ? '#facc15' : '#4b3c0a'} />
                    {selectedImage &&(
                        <Button title="Enhance Image" onPress={enhanceImage} color={colorScheme === 'dark' ? '#facc15' : '#4b3c0a'} disabled={loading} />
                    )}
                </View>

                {/* Loading Indicator */}
                {loading && (
                    <View style={styles.loadingContainer}>
                        <ThemedText>Enhancing Image...</ThemedText>
                    </View>
                )}

                {/* Enhanced Image Display */}
                <View style={styles.imageContainer}>
                    {selectedImage && (
                        <View style={styles.imageBox}>
                            <ThemedText style={styles.imageTitle}>Selected Image:</ThemedText>
                            <Image 
                                source={{ uri: selectedImage }}
                                style={styles.image}
                                resizeMode="contain" 
                            />
                        </View>
                    )}
                    {enhancedImage && (
                        <View style={styles.imageBox}>
                            <ThemedText style={styles.imageTitle}>Enhanced Image:</ThemedText>
                            <Image source={{ uri: enhancedImage }} style={styles.image} resizeMode="contain" />
                        </View>
                    )}
                </View>
            </ParallaxScrollView>
        </ThemedView>
    );
}

const styles = StyleSheet.create({
    headerImage: {
        color: '#808080',
        bottom: -90,
        left: -35,
        position: 'absolute',
    },
    container: {
        flex: 1,
    },
    titleContainer: {
        flexDirection: 'row',
        gap: 8,
    },
    section: {
        marginTop: 20,
        marginBottom: 30,
    },
    label: {
        marginBottom: 4,
    },
    pickerContainer: {
        borderWidth: Platform.OS === 'android' ? 1 : 0,
        borderRadius: 6,
        overflow: 'hidden',
    },
    picker: {
        height: 44,
    },
    modelField: {
        padding: 12,
        backgroundColor: '#eaeaea',
        borderRadius: 8,
        marginTop: 6,
        alignItems: 'center',
    },
    modelText: {
        fontSize: 16,
        fontWeight: '500',
      },
    uploadingContainer: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        marginVertical: 20,
    },
    loadingContainer: {
        alignItems: 'center',
        marginVertical: 16,
    },
    imageContainer: {
        marginTop: 16,
    },
    imageBox: {
        alignItems: 'center',
        marginBottom: 30,
    },
    imageTitle: {
        fontSize: 18,
        marginBottom: 8,
        fontWeight: 'bold',
    },
    image: {
        width: 300,
        height: 300,
        borderRadius: 8,
        borderWidth: 1,
        borderColor: '#ddd',
    },
});
