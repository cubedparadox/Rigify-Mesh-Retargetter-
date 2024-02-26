# Rigify Retargeting Addon

## Purpose
I made this script because I'm using rigify to generate ik rigs for already-rigged characters, by configuring their existing game-ready rigs to be meta-rigs for rigify. However, rigify expects you to weight your mesh to the generated rig itself. 

This addon facilitates the integration of existing game-ready character rigs with Rigify-generated IK rigs in Blender. It streamlines the process of retargeting mesh weights from original metarigs to DEF bones in Rigify rigs, preserving the original setup nondestructively.

## Functionality
- Clones selected meshes, ensuring original data remains untouched.
- Reparents and transfers vertex group weights to match Rigify's DEF-named bones.
- Organizes original and cloned objects into distinct collections for clarity and ease of use.
- Provides a convenient "Retarget Meshes" button within the Armature's Object Data properties for easy access.

## Installation
1. Save the provided Python file to a known location on your computer.
2. Open Blender and go to `Edit > Preferences > Add-ons`.
3. Click `Install...` and navigate to the saved Python file.
4. Select the file and click `Install Add-on`.
5. Enable the addon by ticking the checkbox next to its name.

## Usage
With your metarig selected:
1. Navigate to the Object Data properties of the armature.
2. Click the "Retarget Meshes" button to automatically clone, reparent, and transfer weights to a new Rigify-generated rig.

This addon is designed to work seamlessly with Rigify, simplifying the process of adapting existing rigs for use with advanced IK setups without altering the original mesh and armature data.
