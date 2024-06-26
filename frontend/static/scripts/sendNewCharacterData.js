document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('characterForm');
    const formType = form.name
    switch (formType) {
        case 'add':
            var method = "POST";
            break;
        case 'edit':
            var method = "PATCH";
            break;
    }
    // Enviar el formulario
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Evitar el envío del formulario de forma estándar
        const character_id = document.querySelector('input[name="character_id"]').value || null;
        const characterName = document.getElementById('character_name').value;
        const selectedClass = document.getElementById('class').value;
        const selectedSubclass = document.getElementById('subclass').value;
        const xp = document.getElementById('xp').value;
        const hp = document.getElementById('hp').value;
        const alignment = document.getElementById('alignment').value;
        const background = document.getElementById('background').value;
        const race = document.getElementById('race').value;
        const ac = document.getElementById('ac').value;
        const checkedSkills = Array.from(document.getElementById('allSkills').querySelectorAll('input[type="checkbox"]:checked'))
                                .map(checkbox => checkbox.value);
        const strength = document.querySelector('input[name="totalStrength"]').value;
        const dexterity = document.querySelector('input[name="totalDexterity"]').value;
        const constitution = document.querySelector('input[name="totalConstitution"]').value;
        const intelligence = document.querySelector('input[name="totalIntelligence"]').value;
        const wisdom = document.querySelector('input[name="totalWisdom"]').value;
        const charisma = document.querySelector('input[name="totalCharisma"]').value;
        const personalityTraits = document.getElementById('personality_traits').value;
        const ideals = document.getElementById('ideals').value;
        const bonds = document.getElementById('bonds').value;
        const flaws = document.getElementById('flaws').value;
        const equipment = document.getElementById('equipment').value


        const jsonBody = {
            character_id : character_id,
            characterName: characterName,
            selectedClass: selectedClass,
            selectedSubclass: selectedSubclass,
            xp: xp,
            hp: hp,
            alignment: alignment,
            background: background,
            race: race,
            ac: ac,
            skillProficiencies: checkedSkills,
            strength: strength,
            dexterity: dexterity,
            constitution: constitution,
            intelligence: intelligence,
            wisdom: wisdom,
            charisma: charisma,
            proficienciesLanguages: JSON.stringify({
                languages: null,
                otherProficiencies: null
            }),
            equipment: JSON.stringify({
                equipment: equipment
            }),
            lore: JSON.stringify({
                personalityTraits: personalityTraits,
                ideals: ideals,
                bonds: bonds,
                flaws: flaws
            })
        }
        // Enviar el formulario mediante fetch
        fetch(`/character/${formType}`, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonBody)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Respuesta recibida desde Flask:', data, jsonBody);
            form.removeEventListener('submit', arguments.callee);
            form.submit();
        })
        .catch(error => {
            console.error('Error al enviar el formulario:', error);
            console.log(jsonBody)
        });
    });
});