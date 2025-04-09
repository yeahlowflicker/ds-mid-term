// WebSocketUtility.ts

export interface WebSocketMessage {
    uuid: string;
    enhancement_type: string;
    image: string; // Base64 data URL string
}
  
export type OnMessageHandler = (data: any) => void;

export class WebSocketUtility {
    private ws: WebSocket | null = null;

    // Reconnect configuration:
    private reconnectInterval = 1000; // initial delay in ms
    private maxReconnectInterval = 5000; // maximum delay in ms
    private reconnectAttempts = 0;
    private shouldReconnect = true;

    constructor(private url: string) {}

    /**
     * Opens the WebSocket connection.
     */
    public connect(): void {
        this.ws = new WebSocket(this.url);

        this.ws.onopen = (event) => {
            console.log('WebSocket connection opened:', event);
        };

        this.ws.onmessage = (event) => {
            // console.log('Message received from server:', event.data);
            // Call the onMessage handler to allow client code to process the data.
            this.onMessage(event.data);
        };

        this.ws.onerror = (event) => {
            console.error('WebSocket error:', event);
        };

        this.ws.onclose = (event) => {
            console.log('WebSocket connection closed:', event);
      
            // Attempt to reconnect if flag is enabled.
            if (this.shouldReconnect) {
              this.scheduleReconnect();
            }
        };
    }

    /**
     * Schedule reconnection using an exponential backoff strategy.
     */
    private scheduleReconnect(): void {
        this.reconnectAttempts++;
        const delay = Math.min(this.reconnectInterval * Math.pow(2, this.reconnectAttempts - 1), this.maxReconnectInterval);
        console.log(`Attempting to reconnect in ${delay} ms...`);
        setTimeout(() => {
            this.connect();
        }, delay);
    }

    /**
     * Optional handler for processing messages. Override or assign your own handler.
     */
    public onMessage: OnMessageHandler = (data) => {
        console.log('Received data:', data);
    };

    /**
     * Sends an image with an associated uuid. Reads the image Blob/File as a Base64 data URL.
     *
     * @param uuid - Unique identifier for the image.
     * @param image - A Blob or File representing the image.
     */
    public sendImage(uuid: string, enhancementType: string, image: File | Blob): void {
        if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
        console.error('WebSocket is not open. Please call connect() first.');
        return;
        }

        // Create a FileReader. In React Native, you may need to polyfill or ensure that FileReader is configured.
        const reader = new FileReader();

        reader.onload = () => {
        const dataUrl = reader.result as string;
        const payload: WebSocketMessage = {
            uuid: uuid,
            enhancement_type: enhancementType,
            image: dataUrl,
        };

        // Send the JSON stringified payload.
        this.ws?.send(JSON.stringify(payload));
            console.log('Sent image with UUID:', uuid);
        };

        reader.onerror = (err) => {
            console.error('Failed to read image file:', err);
        };

        // Read the image as a Data URL (Base64).
        reader.readAsDataURL(image);
    }

    /**
     * Closes the WebSocket connection.
     */
    public disconnect(): void {
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
    }
}
  