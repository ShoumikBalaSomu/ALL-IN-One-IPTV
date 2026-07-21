# 📂 Input Folder

Drop your custom playlists here for the engine to collect and merge.

## Supported Formats

| Extension | Description |
|-----------|-------------|
| `.m3u` | Standard M3U playlist |
| `.m3u8` | UTF-8 M3U playlist |
| `.enc` | AES-256-GCM encrypted playlist |

## Encrypted Playlists

To use encrypted `.enc` files:

1. Encrypt your playlist using the [Colab Encryptor](../../colab/encrypt_playlist.ipynb)
2. Upload the `.enc` file here
3. Set `ENCRYPT_KEY` as a GitHub Secret (64-char hex key)
4. The engine will auto-decrypt and merge on next run

## Tips

- Use descriptive filenames: `my_bangla_channels.m3u`, `private_sports.enc`
- Playlists are merged with all public sources automatically
- Files are processed in alphabetical order
- Invalid files are skipped with a warning log

## Example

```
input/
├── .keep                    # This placeholder
├── my_channels.m3u          # Your public channels
├── sports_playlist.m3u      # Sports-specific list
└── private_streams.enc      # Encrypted private streams
```