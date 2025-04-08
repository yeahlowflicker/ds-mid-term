import { View, Text, StyleSheet, SafeAreaView } from 'react-native';
import ParallaxScrollView from '@/components/ParallaxScrollView';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { IconSymbol } from '@/components/ui/IconSymbol';

export default function HomeScreen() {
  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#e0f2ff', dark: '#0f1c26' }}
      headerImage={
        <IconSymbol
          size={300}
          color='#00aaff'
          name="house.fill"
          style={styles.headerImage}
        />
      }
    >
    <ThemedView style={styles.titleContainer}>
      <ThemedText type="title">Image Enhancer</ThemedText>
    </ThemedView>

    <ThemedText>
      Low-resolution images can be enhanced using a variety of techniques, including:
      <ThemedText type="defaultSemiBold"> super-resolution, denoising, and inpainting.</ThemedText>
    </ThemedText>
    <ThemedText>Steps to use:</ThemedText>
    <ThemedText>1. Go to the Enhance tab</ThemedText>
    <ThemedText>2. Select an image from your device</ThemedText>
    <ThemedText>3. Choose a model</ThemedText>
    <ThemedText>4. Tap the Enhance Image button</ThemedText>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  headerImage: {
    color: '#808080',
    bottom: -90,
    left: -35,
    position: 'absolute',
  },
  titleContainer: {
    flexDirection: 'row',
    gap: 8,
  },
});
